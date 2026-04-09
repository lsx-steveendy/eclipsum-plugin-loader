"""
# src/__init__.py
## - The starting point of Eclipsum

## DO NOT RUN THIS ON YOUR OWN unless you know what you're doing. Otherwise run start.bat instead.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.curdir))

import math
import time
from src import logger
import asyncio
from src.plugins import *


LOGGER = logger.getLogger("Eclipsum")




def do_plugins():
    started = time.monotonic()

    candidates = finder._findCandidates()
    if not candidates:
        LOGGER.warning(f"Found 0 plugin candidates. Closing app.")
        sys.exit()

    plugins = preparator._prepareCandidates(candidates)
    if not plugins:
        LOGGER.error(f"All plugins failed to prepare (1/2). Closing app.")
        sys.exit()

    plugins = preparator._preparePlugins(plugins)
    if not plugins:
        LOGGER.error(f"All plugins failed to prepare (2/2). Closing app.")
        sys.exit()

    LOGGER.info(f"Installing dependencies...")
    try:
        dependencies._installPip()
    except Exception as e:
        LOGGER.error(f"Failed to install dependencies.", stack_info=True)
        sys.exit()


    initialized = initializer._initPlugins(plugins)
    ended = time.monotonic()
    LOGGER.info(
        f"Successfully initialized {len(initialized)} plugins! {round(ended-started, 3)}s taken")


async def main():
    await asyncio.to_thread(do_plugins)


if __name__ == "__main__":
    asyncio.run(main())
