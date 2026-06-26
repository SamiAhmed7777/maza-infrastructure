#!/usr/bin/env python3
"""
ElectrumX startup wrapper for MAZA Network.

Defines MAZA coin class and force-registers it by monkey-patching
Coin.lookup_coin_class, bypassing the unreliable __subclasses__()
discovery mechanism.
"""

import sys
import asyncio
import logging

from electrumx.lib.coins import Coin, CoinError
from electrumx.lib import util

# ── Custom MAZA coin class ──
class Mazacoin(Coin):
    NAME = "Mazacoin"
    SHORTNAME = "MAZA"
    NET = "mainnet"
    CHAIN_SIZE = 2_000_000_000
    CHAIN_SIZE_HEIGHT = 2_500_000
    AVG_BLOCK_SIZE = 800
    VALUE_PER_COIN = 100_000_000
    P2PKH_VERBYTE = bytes([50])
    P2SH_VERBYTES = [bytes([9])]
    WIF_BYTE = bytes([224])
    BECH32_HRP = "maza"
    GENESIS_HASH = ('00000c7c73d8ce604178dae13f0fc6ec'
                    '0be3275614366d44b1b4b5c6e238c60c')
    GENESIS_ACTIVATION = 0
    RPC_PORT = 12832
    REORG_LIMIT = 200
    PEER_DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    PEERS = []


class MazacoinTestnet(Mazacoin):
    NET = "testnet"
    SHORTNAME = "tMAZA"
    P2PKH_VERBYTE = bytes([88])
    P2SH_VERBYTES = [bytes([188])]
    WIF_BYTE = bytes([239])
    BECH32_HRP = "tmaza"
    GENESIS_HASH = ('000003ae7f631de18a457fa4fa078e6f'
                    'a8aff38e258458f8189810de5d62cede')
    RPC_PORT = 11832


# ── Force-register: monkey-patch lookup_coin_class ──
_original_lookup = Coin.lookup_coin_class.__func__  # unbound classmethod

def patched_lookup(cls, name, net):
    """Check our custom coins first, then fall back to original discovery."""
    if name.lower() == "mazacoin" and net.lower() == "mainnet":
        return Mazacoin
    if name.lower() == "mazacoin" and net.lower() == "testnet":
        return MazacoinTestnet
    return _original_lookup(cls, name, net)

Coin.lookup_coin_class = classmethod(patched_lookup)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('maza-startup')

# Verify
test_cls = Coin.lookup_coin_class("Mazacoin", "mainnet")
logger.info(f"✅ MAZA coin registered: {test_cls.NAME}/{test_cls.NET} "
            f"(genesis={test_cls.GENESIS_HASH[:16]}...)")
logger.info(f"   Address prefix: {test_cls.P2PKH_VERBYTE.hex()}, "
            f"RPC port: {test_cls.RPC_PORT}")


# ── Start server ──
from electrumx import Controller, Env
from electrumx.lib.util import CompactFormatter, make_logger


def main():
    log_fmt = Env.default('LOG_FORMAT', '%(levelname)s:%(name)s:%(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CompactFormatter(log_fmt))
    srv_logger = make_logger('electrumx', handler=handler, level='INFO')
    srv_logger.info('ElectrumX server starting (MAZA mode)')
    try:
        env = Env()
        srv_logger.info(f'logging level: {env.log_level}')
        srv_logger.setLevel(env.log_level)
        controller = Controller(env)
        asyncio.run(controller.run())
    except Exception:
        srv_logger.exception('ElectrumX server terminated abnormally')
    else:
        srv_logger.info('ElectrumX server terminated normally')


if __name__ == '__main__':
    main()
