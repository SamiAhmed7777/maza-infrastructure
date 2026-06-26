#!/usr/bin/env bash
set -euo pipefail

# ────────────────────────────────────────────────────────────
# Komodo DeFi Framework: enable MAZA coin
#
# Run this AFTER the stack is up and synced.
# Requires: Komodo DeFi Framework (mm2) running with userpass set.
# ────────────────────────────────────────────────────────────

MM2_USERPASS="${MM2_USERPASS:?Set MM2_USERPASS env var first}"
MM2_URL="${MM2_URL:-http://127.0.0.1:7783}"

# ElectrumX server URL (point at your running instance)
ELECTRUM_URL="${ELECTRUM_URL:-127.0.0.1:50001}"
ELECTRUM_SSL_URL="${ELECTRUM_SSL_URL:-127.0.0.1:50002}"

echo "Enabling MAZA on Komodo DeFi Framework..."
echo "  Electrum servers: $ELECTRUM_URL / $ELECTRUM_SSL_URL"

curl -s -X POST "$MM2_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"userpass\": \"$MM2_USERPASS\",
    \"method\": \"enable_electrum\",
    \"mmrpc\": \"2.0\",
    \"params\": {
      \"ticker\": \"MAZA\",
      \"servers\": [
        {\"url\": \"$ELECTRUM_URL\", \"protocol\": \"TCP\"},
        {\"url\": \"$ELECTRUM_SSL_URL\", \"protocol\": \"SSL\"}
      ],
      \"mm2\": 1,
      \"address_format\": {
        \"format\": \"standard\"
      }
    }
  }" | jq .

echo ""
echo "Done. Verify with:"
echo "  curl -s -X POST $MM2_URL -d '{\"userpass\":\"$MM2_USERPASS\",\"method\":\"my_balance\",\"coin\":\"MAZA\"}' | jq ."
