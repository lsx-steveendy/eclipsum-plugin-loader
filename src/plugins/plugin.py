import importlib
import importlib.util
from logging import Logger
import re
import sys
from typing import Literal
from src import logger
import os

LOGGER: Logger = logger.getLogger("Eclipsum/Plugins")

class PluginException(BaseException):
    def __init__(self, *args, what: str|None = None):
        super().__init__(*args)
        self.what: str | None = what

class PluginInfoException(PluginException):
    def __init__(self, *args, what: str|None = None):
        super().__init__(*args, what=what)

class PluginInfo:
    def __init__(self, name):
        spec = importlib.util.spec_from_file_location("INFO", f"{os.path.abspath(os.curdir)}/plugins/{name}/INFO.py")
        info = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(info)

        try:
            self.__NAME = str(info.NAME)
            self.__ID = self.__validateId(info.ID)
            self.__VERSION = self.__validateVersion(info.VERSION)
        except AttributeError as ae:
            print(ae)
            raise PluginInfoException(f"")

    @property
    def VERSION(self):
        return self.__VERSION
    
    @property
    def NAME(self):
        return self.__NAME
    
    @property
    def ID(self):
        return self.__ID
    
    @staticmethod
    def __validateVersion(version: str):
        split: list[str] = version.split(".", maxsplit=2)
        
        try:
            for i in split:
                int(i)
        except:
            raise PluginInfoException(f"Invalid version format. Make sure it follows the MAJOR.MINOR.MAINTENANCE format (e.g. 0.1.0)", what="version")
        
        return ".".join(split)
        

    __id_regex_pattern = re.compile(r"[a-zA-Z\-\_0-9]*")

    @staticmethod
    def __validateId(id: str):
        m: re.Match[str] | None = re.fullmatch(PluginInfo.__id_regex_pattern, id)

        if not m:
            raise PluginInfoException(f"Invalid plugin ID", what="id")
        
        return id


class Plugin:
    def __init__(self, abspath: str):
        self.__abspath: str = abspath
        self.__info: PluginInfo = PluginInfo(self.filename)

    @property
    def path(self):
        return self.__abspath
    
    @property
    def filename(self):
        return os.path.basename(self.__abspath)
    
    @property
    def info(self):
        return self.__info
    
    @property
    def VERSION(self):
        return self.info.VERSION
    
    @property
    def NAME(self):
        return self.info.NAME
    
    @property
    def ID(self):
        return self.info.ID