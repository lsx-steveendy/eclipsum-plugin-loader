import os

from finder import PLUGINS_FOLDER

def _validateCandidates(candidates: list[str]):
    validated = []
    for i in candidates:
        dir = f"{PLUGINS_FOLDER}{i}"