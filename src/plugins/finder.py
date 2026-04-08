from logging import Logger
import os

from src import logger

PLUGINS_FOLDER: str = f"{os.path.abspath(os.curdir)}/plugins/"
LOGGER: Logger = logger.getLogger("Eclipsum/Plugins")

def _findCandidates():
    try:
        os.makedirs(PLUGINS_FOLDER)
    except:
        pass
    try:
        dirs = os.listdir(PLUGINS_FOLDER)
        filtered = [i for i in dirs if os.path.isdir(getAbs(i)) and _isDirPackage(getAbs(i))]
        return filtered
    except NotADirectoryError:
        os.remove(PLUGINS_FOLDER)
        return _findCandidates()
    except PermissionError:
        LOGGER.critical(f"Can't access {PLUGINS_FOLDER}: No permission")
        raise RuntimeError(f"Can't access {PLUGINS_FOLDER}: No permission")

def getAbs(file: str):
    return f"{PLUGINS_FOLDER}{file}"

def _isDirPackage(dir: str):
    return os.path.exists(f"{dir}/__init__.py")