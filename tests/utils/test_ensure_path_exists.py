"""Test the Advent of Code Runner Util ensure_path_exists function"""

# System libraries
from time import sleep

# Pytest libraries
import pytest

# Advent of Code Runner libraries
from aoc_runner.exceptions import DirectoryIsFile
from aoc_runner.utils import _ensure_path_exists


@pytest.mark.parametrize(
    "create",
    [
        (False),
        (True),
    ],
)
@pytest.mark.utils
@pytest.mark.unit
def test_ensure_file_exists_file_does_not_exist(
    tmp_path,
    create,
):
    """Test the utils.ensure_path_exists() function with a
    non-existent file.  The file state should match the
    create parameter.
    '"""

    test_file = tmp_path / "test"
    _ensure_path_exists(path_name="Test Path", path=test_file, create=create)
    assert test_file.exists() == create


@pytest.mark.utils
@pytest.mark.unit
def test_ensure_file_exists_file_does_exist(
    tmp_path,
):
    """Test the utils.ensure_path_exists() function with an
    existing file.  The file should remain unchanged.
    '"""

    test_file = tmp_path / "test"
    test_file.mkdir()
    modified_time = test_file.stat().st_mtime

    sleep(0.01)
    _ensure_path_exists(path_name="Test Path", path=test_file, create=False)
    assert test_file.exists()
    assert test_file.stat().st_mtime == modified_time


@pytest.mark.utils
@pytest.mark.unit
def test_ensure_file_exists_file_is_file(
    tmp_path,
):
    """Test the utils.ensure_path_exists() function with an
    existing file which is a file rather than a directory.
    The exception DirectoryIsFile should be raised.
    '"""

    test_file = tmp_path / "test"
    test_file.touch()

    with pytest.raises(DirectoryIsFile) as ex:
        _ensure_path_exists(path_name="Test Path", path=test_file, create=False)

    ex_msg = str(ex.value)
    assert ex_msg.endswith("to be a directory not a file")
