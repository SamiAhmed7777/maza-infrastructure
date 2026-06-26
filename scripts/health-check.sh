#!/usr/bin/env bash
set -euo pipefail

# ────────────────────────────────────────────────────────────
# Health check for MAZA infrastructure stack
# Usage: ./scripts/health-check.sh
# ────────────────────────────────────────────────────────────

RPC_USER="${RPC_USER:-mazarpc}"
RPC_PASS="${RPC_PASS:-CHANGE_ME_to_a_strong_password}"
RPC_HOST="${RPC_HOST:-127.0.0.1}"
RPC_PORT="${RPC_PORT:-12832}"

echo "═══ MAZA Infrastructure Health Check ═══"
echo ""

# 1. mazad RPC
echo "── mazad ──"
BLOCKCHAIN_INFO=$(curl -sf -u "$RPC_USER:$RPC_PASS" \
  --data-binary '{"jsonrpc":"1.0","id":"health","method":"getblockchaininfo","params":[]}' \
  -H "Content-Type: application/json" \
  "http://$RPC_HOST:$RPC_PORT/" 2>&1) || {
    echo "❌ mazad RPC unreachable at $RPC_HOST:$RPC_PORT"
    exit 1
  }

CONNECTIONS=$(echo "$BLOCKCHAIN_INFO" | jq -r '.result.connections // "N/A"')
BLOCKS=$(echo "$BLOCKCHAIN_INFO" | jq -r '.result.blocks // "N/A"')
HEADERS=$(echo "$BLOCKCHAIN_INFO" | jq -r '.result.headers // "N/A"')
VERIFICATION=$(echo "$BLOCKCHAIN_INFO" | jq -r '.result.verificationprogress // "N/A"')
SIZE_ON_DISK=$(echo "$BLOCKCHAIN_INFO" | jq -r '.result.size_on_disk // "N/A"')

if [ "$CONNECTIONS" -gt 0 ] 2>/dev/null; then
  echo "✅ Connected — $CONNECTIONS peers"
else
  echo "⚠️  No peers connected"
fi
echo "   Blocks:   $BLOCKS"
echo "   Headers:  $HEADERS"
echo "   Sync:     $(echo "$VERIFICATION" | awk '{printf "%.2f%%", $1*100}')"
echo "   Disk:     $(( SIZE_ON_DISK / 1024 / 1024 )) MB"

# 2. ElectrumX
echo ""
echo "── ElectrumX ──"
ELECTRUM_HOST="${ELECTRUM_HOST:-127.0.0.1}"
ELECTRUM_PORT="${ELECTRUM_PORT:-50001}"
if nc -z -w3 "$ELECTRUM_HOST" "$ELECTRUM_PORT" 2>/dev/null; then
  echo "✅ ElectrumX reachable on $ELECTRUM_HOST:$ELECTRUM_PORT"
else
  echo "⚠️  ElectrumX not responding on $ELECTRUM_HOST:$ELECTRUM_PORT"
fi

echo ""
echo "═══ Health check complete ═══"
