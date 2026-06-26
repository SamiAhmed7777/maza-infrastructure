#!/usr/bin/env bash
set -euo pipefail

# ────────────────────────────────────────────────────────────
# Quick maza-cli wrapper for Docker
# Usage: ./scripts/maza-cli.sh getblockchaininfo
# ────────────────────────────────────────────────────────────

docker exec -it mazad maza-cli "$@"
