import logging
import os

os.mkdir("logs")

class Formatter(logging.Formatter):
    def __init__(self):
        super().__init__("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")

class Handler(logging.FileHandler):
    def __init__(self, filename, mode = "a", encoding = None, delay = False, errors = None):
        super().__init__(filename, mode, encoding, delay, errors)

__loggers = {}
def getLogger(id: str):
    return __loggers.get(id, __createLogger(id))

def __createLogger(id: str):
    logger = logging.getLogger(id)
    logger.addHandler(Handler("logs/latest.log"))
    __loggers[id] = logger
    return logger
