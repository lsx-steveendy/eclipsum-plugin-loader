import logging
import os

if not os.path.exists("logs"):
    os.mkdir("logs")

class Formatter(logging.Formatter):
    def __init__(self):
        super().__init__(fmt="%(asctime)s [%(name)s] [%(levelname)s] %(message)s")

class Handler(logging.FileHandler):
    def __init__(self, filename, mode = "a", encoding = None, delay = False, errors = None):
        super().__init__(filename, mode, encoding, delay, errors)
        self.formatter = Formatter()

logging.basicConfig(level=logging.INFO, handlers=[Handler("logs/latest.log")])

__loggers: dict[str, logging.Logger] = {}
def getLogger(id: str) -> logging.Logger:
    return __loggers.get(id, __createLogger(id))

def __createLogger(id: str):
    logger: logging.Logger = logging.getLogger(id)
    __loggers[id] = logger
    return logger
