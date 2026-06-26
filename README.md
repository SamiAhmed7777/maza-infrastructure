# MAZA Network Infrastructure

Full-stack infrastructure for the [MAZA Network](https://github.com/MazaCoin/maza) (MazaCoin) — a Litecoin Cash fork with MinotaurX + Hive mining, originally launched in 2014.

This repo provides everything needed to run a self-hosted MAZA backend:

- **`mazad`** — full node daemon, compiled from source via multi-stage Docker build
- **ElectrumX** — indexer/light-wallet server with a custom MAZA coin class
- **Komodo DeFi Framework** — coin config + enablement script for atomic swap integration

## Architecture

```
                    ┌─────────────┐
                    │   mazad     │  P2P :12835
                    │  (full node)│  RPC :12832
                    └──────┬──────┘
                           │ JSON-RPC
                    ┌──────┴──────┐
                    │  ElectrumX  │  TCP :50001
                    │  (indexer)  │  SSL :50002
                    └──────┬──────┘
                           │ Electrum protocol
                    ┌──────┴──────┐
                    │  Komodo DFi │  Atomic swap DEX
                    │  Framework  │
                    └─────────────┘
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/SamiAhmed7777/maza-infrastructure.git
cd maza-infrastructure

# 2. Set your RPC password (do NOT keep the default!)
sed -i 's/CHANGE_ME_to_a_strong_password/YOUR_SECURE_PASSWORD/g' \
  mazad/maza.conf \
  electrumx/electrumx.conf \
  docker-compose.yml \
  komodo-defi/MAZA.json

# 3. Build and start
docker compose up -d --build

# 4. Watch the node sync (first sync takes hours)
docker logs -f mazad

# 5. Check health
./scripts/health-check.sh
```

## Network Parameters (from source)

| Parameter         | Mainnet           | Testnet           |
|-------------------|--------------------|--------------------|
| P2P port          | 12835             | 11835             |
| RPC port          | 12832             | 11832             |
| PubKey prefix     | 50 (`0x32`)       | 88 (`0x58`)       |
| P2SH prefix       | 9 (`0x09`)        | 188 (`0xBC`)      |
| WIF prefix        | 224 (`0xE0`)      | 239 (`0xEF`)      |
| Bech32 HRP        | `maza`            | `tmaza`           |
| Network magic     | `f8 b5 03 df`     | `05 fe a9 01`     |
| Block time        | 2 minutes          | 2 minutes          |
| Genesis hash      | `00000c7c...`     | `000003ae...`     |

## Components

### mazad/

Multi-stage Dockerfile that compiles `mazad` from the [MazaCoin/maza](https://github.com/MazaCoin/maza) source tree. The build stage installs all dependencies (Boost, OpenSSL, libevent, BerkeleyDB 4.8), compiles with `--without-gui --without-miniupnpc`, then copies the stripped binary into a minimal runtime image.

**Build time:** ~20–40 min on a 4-core machine (Bitcoin Core-style C++ build).

### electrumx/

ElectrumX 1.16 (last generic version before the BSV fork) with a custom MAZA coin class injected at startup. The `coins_maza.py` module defines `Mazacoin(Coin)` with the correct address prefixes, genesis hash, and RPC port — no patching of electrumx source needed.

**Sync time:** Depends on chain height. MAZA has ~2.5M blocks; expect 2–6 hours for full indexing after mazad is synced.

### komodo-defi/

- `MAZA.json` — Komodo DeFi Framework UTXO coin configuration
- `enable_maza.sh` — script to enable MAZA on a running KDF instance via the Electrum protocol

After the stack is running and synced, point Komodo DeFi Framework at your local ElectrumX server:

```bash
export MM2_USERPASS="your_kdf_userpass"
./komodo-defi/enable_maza.sh
```

### scripts/

- `health-check.sh` — verify mazad + ElectrumX status
- `maza-cli.sh` — wrapper for `maza-cli` inside the container

## Useful Commands

```bash
# Check sync progress
./scripts/maza-cli.sh getblockchaininfo

# Get peer info
./scripts/maza-cli.sh getpeerinfo

# Stop node cleanly
docker exec mazad maza-cli stop

# Rebuild after code changes
docker compose up -d --build
```

## Why This Exists

There is **no public Electrum server for MAZA**. No `electrum-maza` repo exists, no listed server, no DNS seed entry in the Komodo DeFi Framework coins file. This repo fills that gap — you run the entire backend stack yourself, then any Electrum-compatible wallet or Komodo DEX can connect to it.

## License

MIT (same as MAZA Core). The upstream MAZA source, ElectrumX, and Komodo DeFi Framework each retain their respective licenses.
