"""Test the Advent of Code Runner Util Color class"""

# System libraries
# from time import sleep

# Pytest libraries
import pytest

# Advent of Code Runner libraries
from aoc_runner.utils import Color


@pytest.mark.utils
@pytest.mark.unit
def test_color_as_dict(color_name_code_dict):
    """Test the color_dict class method"""

    color = Color()
    color_dict = color.as_dict()

    assert isinstance(color_dict, dict)
    for color_name, color_code in color_dict.items():
        assert isinstance(color_name, str)
        assert color_name == color_name.upper()
        assert isinstance(color_code, str)
        assert color_name in color_name_code_dict.keys()
        assert color_code == color_name_code_dict.get(color_name)


@pytest.mark.utils
@pytest.mark.unit
def test_color_color_names(color_name_list):
    """Test the color_names class method"""

    color = Color()
    color_list = color.color_names()

    assert isinstance(color_list, list)
    for color in color_list:
        assert isinstance(color, str)
        assert color == color.upper()
        assert color in color_name_list


@pytest.mark.utils
@pytest.mark.unit
def test_color_color_values(color_code_list):
    """Test the color_values class method"""

    color_code = Color()
    color_codes = color_code.color_codes()

    assert isinstance(color_codes, list)
    for color_code in color_codes:
        assert isinstance(color_code, str)
        assert color_code in color_code_list


@pytest.mark.utils
@pytest.mark.unit
def test_color_get_color_code_valid(get_color_name_code_list):
    """Test the get_color_code class method with valid color names"""

    color_name, color_code = get_color_name_code_list
    color = Color()
    color_code_value = color.get_color_code(color_name=color_name)
    assert isinstance(color_code, str)
    assert color_code_value == color_code


@pytest.mark.utils
@pytest.mark.unit
def test_color_get_color_code_invalid(get_invalid_colors):
    """Test the get_color_code class method with invalid color names"""

    color_name = get_invalid_colors
    color = Color()
    color_code = color.get_color_code(color_name=color_name)
    assert color_code is None


@pytest.mark.utils
@pytest.mark.unit
def test_color_validate_color_code_valid(get_color_code_list):
    """Test the validate_color_code class method with valid color codes"""

    color_value = get_color_code_list
    color = Color()
    color_valid = color.validate_color_code(color_code=color_value)
    assert isinstance(color_valid, bool)
    assert color_valid


@pytest.mark.utils
@pytest.mark.unit
def test_color_validate_color_code_invalid(get_invalid_colors):
    """Test the validate_color class method with invalid color codes"""

    color_value = get_invalid_colors
    color = Color()
    color_valid = color.validate_color_code(color_code=color_value)

    assert isinstance(color_valid, bool)
    assert not color_valid


@pytest.mark.utils
@pytest.mark.unit
def test_color_validate_color_name_valid(get_color_name_list):
    """Test the validate_color_name class method with valid color names"""

    color_name = get_color_name_list
    color = Color()
    color_valid = color.validate_color_name(color_name=color_name)
    assert isinstance(color_valid, bool)
    assert color_valid


@pytest.mark.utils
@pytest.mark.unit
def test_color_validate_color_name_valid(get_invalid_colors):
    """Test the validate_color_name class method with invalid color names"""

    color_name = get_invalid_colors
    color = Color()
    color_valid = color.validate_color_name(color_name=color_name)
    assert isinstance(color_valid, bool)
    assert not color_valid
