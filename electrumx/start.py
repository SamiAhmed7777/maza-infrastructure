#!/usr/bin/env python3
"""
ElectrumX startup wrapper for MAZA Network.

Imports the custom coin class so ElectrumX can discover it,
then launches the server using the same entry point as the
installed electrumx_server console script.
"""

import sys
import asyncio
import logging

# Register custom MAZA coin class with ElectrumX's Coin hierarchy
sys.path.insert(0, "/app")
import coins_maza  # noqa: F401 - side effect: registers Mazacoin class

from electrumx import Controller, Env
from electrumx.lib.util import CompactFormatter, make_logger


def main():
    log_fmt = Env.default('LOG_FORMAT', '%(levelname)s:%(name)s:%(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CompactFormatter(log_fmt))
    logger = make_logger('electrumx', handler=handler, level='INFO')

    logger.info('ElectrumX server starting (MAZA mode)')
    try:
        if sys.version_info < (3, 7):
            raise RuntimeError('ElectrumX requires Python 3.7 or greater')
        env = Env()
        logger.info(f'logging level: {env.log_level}')
        logger.setLevel(env.log_level)
        controller = Controller(env)
        asyncio.run(controller.run())
    except Exception:
        logger.exception('ElectrumX server terminated abnormally')
    else:
        logger.info('ElectrumX server terminated normally')


if __name__ == '__main__':
    main()
