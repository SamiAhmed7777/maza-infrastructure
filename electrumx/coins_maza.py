"""
Custom MAZA Network coin definition for ElectrumX.

MAZA is a Bitcoin/Litecoin Cash fork with MinotaurX + Hive mining.
This class registers itself with ElectrumX's Coin hierarchy so the
COIN config parameter can reference it as "Mazacoin".

Network parameters sourced from MazaCoin/maza chainparams.cpp:
  - P2P port: 12835
  - RPC port: 12832
  - PubKey address prefix: 50 (0x32)  -> addresses start with 'M'
  - P2SH address prefix: 9 (0x09)
  - WIF prefix: 224 (0xE0)
  - Bech32 HRP: "maza"
  - Genesis: 00000c7c73d8ce604178dae13f0fc6ec0be3275614366d44b1b4b5c6e238c60c
"""

from electrumx.lib.coins import Coin


class Mazacoin(Coin):
    NAME = "Mazacoin"
    SHORTNAME = "MAZA"
    NET = "mainnet"

    # Chain statistics (estimates as of 2026)
    CHAIN_SIZE = 2_000_000_000        # ~2 GB estimated
    CHAIN_SIZE_HEIGHT = 2_500_000
    AVG_BLOCK_SIZE = 800              # Low-volume chain

    # Monetary
    VALUE_PER_COIN = 100_000_000      # 8 decimal places, same as BTC

    # Address prefixes (from chainparams.cpp base58Prefixes)
    P2PKH_VERBYTE = bytes([50])       # 0x32 -> mainnet addresses
    P2SH_VERBYTES = [bytes([9])]      # 0x09
    WIF_BYTE = bytes([224])           # 0xE0

    # Bech32
    BECH32_HRP = "maza"

    # Network
    GENESIS_HASH = ('00000c7c73d8ce604178dae13f0fc6ec'
                    '0be3275614366d44b1b4b5c6e238c60c')
    GENESIS_ACTIVATION = 0
    RPC_PORT = 12832
    REORG_LIMIT = 200

    # Electrum protocol ports (standard defaults)
    PEER_DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    PEERS = []


class MazacoinTestnet(Mazacoin):
    NET = "testnet"
    SHORTNAME = "tMAZA"
    P2PKH_VERBYTE = bytes([88])       # 0x58
    P2SH_VERBYTES = [bytes([188])]    # 0xBC
    WIF_BYTE = bytes([239])           # 0xEF
    BECH32_HRP = "tmaza"
    GENESIS_HASH = ('000003ae7f631de18a457fa4fa078e6f'
                    'a8aff38e258458f8189810de5d62cede')
    RPC_PORT = 11832
    PEERS = []


# Self-registration: Coin.lookup_coin_class() scans all loaded subclasses
# of Coin. Importing this module makes Mazacoin discoverable.
