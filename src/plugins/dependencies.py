import asyncio
from pydoc import describe
import re
import subprocess
import sys
import traceback

__FINISHED = False


class Dependencies:
    """do not"""
    _pip_regex_pattern = re.compile(
        r"((([a-zA-Z\-\_\.]+)(?:==|<=|>=)(?:\d+\.\d+\.\d+|\d+\.\d+|\d+)|([a-zA-Z\-\_\.]+))[a-zA-Z0-9\\\.\-\=\+\_\(\)\^\%\$\#\@\!\&\*\|\.\,\/\[\]\{\}\'\;\:]*)")

    @staticmethod
    def _validatePipArg(arg: str):
        m: re.Match[str] | None = re.fullmatch(
            Dependencies._pip_regex_pattern, arg)
        return m

    _pip: dict[str, Pip] = {}

class Pip:
    def __init__(self, match: re.Match[str]):
        self.arg = match.group()
        self.raw_arg = match.group(1)  # no additional arguments
        self.name = match.group(2) or match.group(3)

# Equals to "py -m pip install {arg}"
# Make sure arg has a format of "{name}", "{name}=={ver}", "{name}>={ver}" or "{name}<={ver}"
# You can also add additional
# https://pip.pypa.io/en/latest/user_guide/


def dependencyPip(arg: str):
    match = Dependencies._validatePipArg(arg)
    if not match:
        raise RuntimeError(f"Invalid pip argument: {arg}")

    pip_dep = Pip(match)
    duplicate = Dependencies._pip.get(pip_dep.name)
    if duplicate:
        raise RuntimeError(
            f"Dependency was already registered: {duplicate.arg} -> {pip_dep.arg}")
    Dependencies._pip[pip_dep.name] = pip_dep


def _installPip():
    if __FINISHED:
        return
    if not Dependencies._pip:
        return
    proc: subprocess.Popen[bytes] = subprocess.Popen(
        [".venv/Scripts/activate.bat;", sys.executable, "-m", "pip", "install", *[i.arg for i in Dependencies._pip.values()]])


async def _installPip_async():
    await asyncio.to_thread(_installPip())
