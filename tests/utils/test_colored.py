"""Test the Advent of Code Runner Util colored method"""

# Pytest libraries
import pytest

# Advent of Code Runner libraries
from aoc_runner.utils import colored, Color


@pytest.mark.utils
@pytest.mark.unit
def test_colored_no_input():
    """Test the colored function"""

    test_text = "Test Text"
    colored_text = colored(txt=test_text, color_name=None)
    assert test_text == colored_text


@pytest.mark.utils
@pytest.mark.unit
def test_colored_valid_input(
    get_color_name_code_list,
):
    """Test the colored function with valid input"""

    color_name, color_value = get_color_name_code_list
    test_text = "Test Text"
    colored_text = colored(txt=test_text, color_name=color_name)
    assert colored_text == f"{color_value}{test_text}{Color.END}"


@pytest.mark.utils
@pytest.mark.unit
def test_colored_invalid_input(
    get_invalid_colors,
):
    """Test the colored function with invalid input"""

    color_name = get_invalid_colors
    test_text = "Test Text"
    colored_text = colored(txt=test_text, color_name=color_name)
    assert colored_text == test_text
