"""Pytest fixtures for the Advent of Code Runner package"""

# Pytest libraries
import pytest


@pytest.fixture
def runner_dir(
    tmp_path,
):
    """Build a temporary directory tree for use as the Advent of Code
    Runner storage tree
    """
    runner_dir = tmp_path / "aoc_runner"
    runner_dir.mkdir()
    yield runner_dir


@pytest.fixture
def runner_auth_dir(
    runner_dir,
):
    """Build a temporary directory tree for use as the Advent of Code
    Runner storage tree
    """
    auth_dir = runner_dir / "auth"
    auth_dir.mkdir()
    yield auth_dir


@pytest.fixture
def runner_cache_dir(
    runner_dir,
):
    """Build a temporary directory tree for use as the Advent of Code
    Runner storage tree
    """
    cache_dir = runner_dir / "cache"
    cache_dir.mkdir()
    yield cache_dir


@pytest.fixture
def runner_users_dir(
    runner_dir,
):
    """Build a temporary directory tree for use as the Advent of Code
    Runner storage tree
    """
    users_dir = runner_dir / "users"
    users_dir.mkdir()
    yield users_dir


@pytest.fixture
def user_module_dir_patch(
    runner_auth_dir,
    runner_users_dir,
    monkeypatch,
):
    """Monkey patch the users directories"""

    monkeypatch.setattr("aoc_runner.user.AOC_RUNNER_AUTH_DIR", runner_auth_dir)
    monkeypatch.setattr("aoc_runner.user.AOC_RUNNER_USERS_DIR", runner_users_dir)
