"""Test the Advent of Code Runner Util get_soup method"""

# System libraries
# from time import sleep

# Third-party libraries
from bs4 import BeautifulSoup

# Pytest libraries
import pytest

# Advent of Code Runner libraries
from aoc_runner.utils import get_soup


@pytest.mark.utils
@pytest.mark.unit
def test_get_soup_text_input():
    """Test the get_soup function with HTML input"""

    soup = get_soup("plain test")
    print(f"Soup type: {type(soup)}")
    assert isinstance(soup, BeautifulSoup)
    # colored_text = colored(txt=test_text, color_name=None)
    # assert test_text == colored_text


@pytest.mark.utils
@pytest.mark.unit
def test_get_soup_no_input():
    """Test the get_soup function with HTML input"""

    with pytest.raises(TypeError):
        _ = get_soup(None)
