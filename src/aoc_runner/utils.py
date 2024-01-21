"""General utilities used by Advent of Code Runner"""

# System libraries
from functools import cache
import logging

# Third-party libraries
from bs4 import BeautifulSoup


log = logging.getLogger(__name__)


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
    def color_names(cls) -> list[str]:
        """Return the defined color names as a list"""
        return [
            # key for key in cls.__dict__.keys()
            key
            for key in cls.__dict__
            if not key.startswith("__") and key[:2] == key[:2].upper()
        ]

    @classmethod
    def color_values(cls) -> list[str]:
        """Return the defined color values as a list"""
        return [
            value
            for key, value in cls.__dict__.items()
            if isinstance(value, str) and key in cls.color_names()
        ]

    @classmethod
    def get_color_code(cls, color_name) -> str:
        """Return the ANSI terminal color code associated with a defined name"""
        color_code = [
            value for key, value in cls.__dict__.items() if key == color_name.upper()
        ]
        return color_code[0]

    @classmethod
    def validate_color(cls, color_code) -> bool:
        """Validate that the color code provided is defined"""
        return color_code in cls.color_values()


color = Color()


def colored(txt: str, color: str | None) -> str:
    """Add color formatting to the provided text"""
    if color is None:
        return txt

    if color.upper() in Color().color_names():
        color_name = color
        color = Color().get_color_code(color)
        log.debug("Color %s was translated", color_name)

    if not Color().validate_color(color):
        log.debug("Color %s not defined -- continuing", color)

    return f"{color}{txt}{Color().END}"


@cache
def get_soup(html):
    """Get am instance of a Beautiful Soup parsed HTML page"""
    soup = BeautifulSoup(html, "html.parser")
    return soup


if __name__ == "__main__":
    SAMPLE_TEXT = "Sample text"
    print(f"Color names: {Color().color_names()}")
    print(f"Color values: {Color().color_values()}")
    print(colored(txt=SAMPLE_TEXT, color=color.RED))
    print(colored(txt=SAMPLE_TEXT, color="blue"))
    print(colored(txt=SAMPLE_TEXT, color="hazy"))
