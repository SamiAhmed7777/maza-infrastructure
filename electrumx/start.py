#!/usr/bin/env python3
"""
ElectrumX startup wrapper for MAZA Network.

Imports the custom coin class so ElectrumX can discover it,
then launches the server with the standard electrumx_server entrypoint.
"""

import sys

# Register custom MAZA coin class with ElectrumX's Coin hierarchy
sys.path.insert(0, "/app")
import coins_maza  # noqa: F401 - side effect: registers Mazacoin class

# Launch electrumx_server normally
from electrumx.server.server import main
sys.argv = ["electrumx_server"]
main()
