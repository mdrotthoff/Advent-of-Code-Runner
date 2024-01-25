"""General utilities used by Advent of Code Runner"""

# System libraries
from functools import cache
import logging
from pathlib import Path

# Third-party libraries
from bs4 import BeautifulSoup

# Advent of Code Runner libraries
from .exceptions import DirectoryIsFile

log = logging.getLogger(__name__)


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


class Color:
    """Defines a class to set colors on a terminal window"""

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    @classmethod
    def as_dict(cls) -> dict[str, str]:
        """Return the defined color names as a list"""
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("__") and key[:2] == key[:2].upper()
        }

    @classmethod
    def color_names(cls) -> list[str]:
        """Return the defined color names as a list"""
        return [key for key, _ in cls.as_dict().items()]

    @classmethod
    def color_codes(cls) -> list[str]:
        """Return the defined color codes as a list"""
        return [value for _, value in cls.as_dict().items()]

    @classmethod
    def get_color_code(cls, color_name) -> str:
        """Return the ANSI terminal color code associated with a defined name"""
        color_code = [
            value for key, value in cls.__dict__.items() if key == color_name.upper()
        ]
        return color_code[0] if color_code else None

    @classmethod
    def validate_color_code(cls, color_code) -> bool:
        """Validate that the color code provided is defined"""
        return color_code in cls.color_codes()

    @classmethod
    def validate_color_name(cls, color_name) -> bool:
        """Validate that the color code provided is defined"""
        return color_name in cls.color_names()


color = Color()


def colored(txt: str, color_name: str | None) -> str:
    """Add color formatting to the provided text"""
    if color_name is None:
        print("Color name was None")
        return txt

    if color_name.upper() not in Color().color_names():
        print("Color %s not defined -- continuing", color_name)
        log.debug("Color %s not defined -- continuing", color_name)
        return txt

    color_code = Color().get_color_code(color_name=color_name)
    log.debug("Color %s was translated", color_name)

    return f"{color_code}{txt}{Color().END}"


@cache
def get_soup(html):
    """Get am instance of a Beautiful Soup parsed HTML page"""
    soup = BeautifulSoup(html, "html.parser")
    return soup


# if __name__ == "__main__":
#     SAMPLE_TEXT = "Sample text"
#     print(f"Color names: {Color().color_names()}")
#     print(f"Color values: {Color().color_values()}")
#     print(colored(txt=SAMPLE_TEXT, color=color.RED))
#     print(colored(txt=SAMPLE_TEXT, color="blue"))
#     print(colored(txt=SAMPLE_TEXT, color="hazy"))
