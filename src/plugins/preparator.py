import importlib
import importlib.util
from logging import Logger
import os

from .finder import PLUGINS_FOLDER
from src import logger
from src.plugins.plugin import Plugin, PluginException

LOGGER: Logger = logger.getLogger("Eclipsum/Plugins")

def _prepareCandidates(candidates: list[str]):
    prepared = []
    for i in candidates:
        dir = f"{PLUGINS_FOLDER}{i}"
        LOGGER.info(f"Preparing {i} (1/2)")

        try:
            plugin = Plugin(dir)
        except PluginException as pe:
            LOGGER.error(*pe.args, stack_info=True)
            continue

        prepared.append(plugin)

    return prepared

def _preparePlugins(plugins: list[Plugin]):
    prepared = []
    for i in plugins:
        LOGGER.info(f"Preparing {i.ID} (2/2)")

        try:
            spec = importlib.util.spec_from_file_location("PREP", f"{os.path.abspath(os.curdir)}/plugins/{i.filename}/PREP.py")
            info = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(info)
        except PluginException as pe:
            LOGGER.error(*pe.args, stack_info=True)
            continue

        prepared.append(i)

    return prepared