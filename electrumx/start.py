#!/usr/bin/env python3
"""
ElectrumX startup wrapper for MAZA Network.

Defines the custom MAZA coin class inline and verifies it's registered
with ElectrumX's Coin hierarchy before starting the server.
"""

import sys
import asyncio
import logging

from electrumx.lib.coins import Coin
from electrumx.lib.hash import double_sha256, Base58, HASHX_LEN
from electrumx.lib.script import ScriptPubKey
from hashlib import sha256
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


# ── Verify registration ──
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('maza-startup')

# Debug: list all discovered coin classes
all_subs = util.subclasses(Coin)
logger.info(f"Registered coin classes: {[(c.NAME, c.NET) for c in all_subs]}")

try:
    test_cls = Coin.lookup_coin_class("Mazacoin", "mainnet")
    logger.info(f"✅ MAZA coin class verified: {test_cls.NAME}/{test_cls.NET}")
except Exception as e:
    logger.error(f"❌ MAZA coin lookup failed: {e}")
    # Force-register by patching lookup
    logger.warning("Force-registering Mazacoin...")
    import electrumx.lib.coins as coins_mod
    # Inject into the module namespace so subclasses() finds it
    coins_mod.Mazacoin = Mazacoin
    sys.exit(1)


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
