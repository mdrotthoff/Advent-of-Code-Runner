"""Common Advent of Code Runner Config fixtures"""

# Pytest libraries
import pytest


@pytest.fixture
def make_ensure_path_exists(
    request,
):
    """Create a factory which allows for dynamic loading of token data from file"""

    def make(
        *args,
        **kwargs,
    ) -> None:
        """Load the cached user setting response from the Advent of Code servers"""

    return make


@pytest.fixture
def ensure_path_exists(
    make_ensure_path_exists,
    monkeypatch,
):
    """Monkey patch the http_client.get() to be a local operation"""

    monkeypatch.setattr("aoc_runner.utils._ensure_path_exists", make_ensure_path_exists)
