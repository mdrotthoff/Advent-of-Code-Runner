"""Advent of Code Runner configuration definitions"""

# System libraries
import logging
from os import environ
from pathlib import Path
from zoneinfo import ZoneInfo

# TODO: Remove conditional import at development is complete
# Advent of Code Runner libraries
from .exceptions import DirectoryIsFile

# if __name__ == "__main__":
#     from exceptions import DirectoryIsFile
# else:
#     from .exceptions import DirectoryIsFile

__version__ = "0.0.1"

log = logging.getLogger(__name__)


"""Defined the various environment variables used"""
RUNNER_AUTH: str = "AOC_RUNNER_AUTH_DIR"
RUNNER_CACHE: str = "AOC_RUNNER_CACHE_DIR"
RUNNER_DIR: str = "AOC_RUNNER_DIR"
RUNNER_HOME: str = "AOC_RUNNER_PROJECT_HOME"
RUNNER_USERS: str = "AOC_RUNNER_USERS_DIR"


def _ensure_path_exists(path_name: str, path: Path, create: bool = True) -> None:
    """Ensure that the specified directory path exists and is
    a directory
    """
    log.debug("Setting %s to %s", path_name, path)
    print(f"Setting {path_name} to {str(path)}")

    if path.exists():
        if path.is_file():
            raise DirectoryIsFile(f"Expected {str(path)} to be a directory not a file")
    elif create:
        path.mkdir(parents=True, exist_ok=True)


# Set the default location for the Advent of Code Runner to store
# the various directories required
if RUNNER_DIR not in environ:
    if RUNNER_HOME in environ:
        AOC_RUNNER_DIR = Path(environ.get(RUNNER_HOME), ".config", ".aoc_runner")
    else:
        AOC_RUNNER_DIR = Path("~", ".config", ".aoc_runner").expanduser()
else:
    AOC_RUNNER_DIR = Path(environ.get(RUNNER_DIR))
_ensure_path_exists(path_name=RUNNER_DIR, path=AOC_RUNNER_DIR, create=True)

# Set the default home of the Advent of Code project
if RUNNER_HOME not in environ:
    AOC_RUNNER_PROJECT_HOME = Path.cwd().parent
else:
    AOC_RUNNER_PROJECT_HOME = Path(environ.get(RUNNER_HOME))
_ensure_path_exists(path_name=RUNNER_HOME, path=AOC_RUNNER_PROJECT_HOME, create=False)


# Set the default folder where user data is cached.  This includes
# any answers, prose, etc. that are user specific
if RUNNER_USERS not in environ:
    AOC_RUNNER_USERS_DIR = AOC_RUNNER_DIR / "users"
else:
    AOC_RUNNER_USERS_DIR = Path(environ.get(RUNNER_USERS))
_ensure_path_exists(path_name=RUNNER_USERS, path=AOC_RUNNER_USERS_DIR, create=True)


# Set the default folder where general data is cached.  This includes
# example data, general prose, etc.
if RUNNER_CACHE not in environ:
    AOC_RUNNER_CACHE_DIR = AOC_RUNNER_DIR / "cache"
else:
    AOC_RUNNER_CACHE_DIR = Path(environ.get(RUNNER_CACHE))
_ensure_path_exists(path_name=RUNNER_CACHE, path=AOC_RUNNER_CACHE_DIR, create=True)


# Set the default folder where general data is cached.  This includes
# example data, general prose, etc.
if RUNNER_AUTH not in environ:
    AOC_RUNNER_AUTH_DIR = AOC_RUNNER_DIR / ".auth"
else:
    AOC_RUNNER_AUTH_DIR = Path(environ.get(RUNNER_AUTH))
_ensure_path_exists(path_name=RUNNER_AUTH, path=AOC_RUNNER_AUTH_DIR, create=True)


AOC_DOMAIN = "https://adventofcode.com"
AOC_TZ = ZoneInfo("America/New_York")
