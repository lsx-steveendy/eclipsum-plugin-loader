import importlib
from logging import Logger

from src import logger
from src.plugins.plugin import Plugin, PluginException

LOGGER: Logger = logger.getLogger("Eclipsum/Plugins")

def _initPlugins(plugins: list[Plugin]):
    initialized = []
    for i in plugins:
        LOGGER.info(f"Initializing {i.ID}")
        try:
            importlib.import_module(f".{i.filename}", f"plugins")
        except PluginException as pe:
            LOGGER.error(*pe.args, stack_info=True, stacklevel=3)
            continue

        initialized.append(i)

    return initialized
