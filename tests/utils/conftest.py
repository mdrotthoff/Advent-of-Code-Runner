"""Common Advent of Code Runner Utils fixtures"""

# Pytest libraries
import pytest


VALID_COLORS = {
    "PURPLE": "\033[95m",
    "CYAN": "\033[96m",
    "DARKCYAN": "\033[36m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}

INVALID_COLORS = ["Hazy", "Cloudy", "Meatballs", "Rain"]


def get_color_name_code_list():
    """Yield each name & code defined in the Color class"""

    return list(VALID_COLORS.items())


@pytest.fixture
def color_name_code_list():
    """Return a list of color names & associated codes"""

    return get_color_name_code_list()


@pytest.fixture
def color_name_code_dict():
    """Return a dictionary of color names & associated codes"""

    return VALID_COLORS


def get_color_name_list():
    """Get a list of the defined color names"""

    return list(VALID_COLORS.keys())


@pytest.fixture
def color_name_list():
    """Return a list of color names & associated codes"""

    return get_color_name_list()


def get_color_code_list():
    """Get a list of the defined color codes"""

    return list(VALID_COLORS.values())


@pytest.fixture
# def color_name_code_list():
def color_code_list():
    """Return a list of color names & associated codes"""

    return get_color_code_list()


def pytest_generate_tests(
    metafunc,
):
    """Generate parametrized test cases for selected
    list of values
    """

    for fixture in metafunc.fixturenames:
        if fixture == "get_color_name_code_list":
            test_data = get_color_name_code_list()
            metafunc.parametrize(fixture, test_data)
        elif fixture == "get_color_name_list":
            test_data = get_color_name_list()
            metafunc.parametrize(fixture, test_data)
        elif fixture == "get_color_code_list":
            test_data = get_color_code_list()
            metafunc.parametrize(fixture, test_data)
        elif fixture == "get_invalid_colors":
            metafunc.parametrize(fixture, INVALID_COLORS)
