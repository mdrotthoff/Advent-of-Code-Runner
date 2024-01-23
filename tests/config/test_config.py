"""Test the Advent of Code Runner Config module"""

# System Libraries
from importlib import reload
from pathlib import Path
import sys

# Pretty Print libraries
from pprint import pprint

# Import Pytest libraries
import pytest


@pytest.mark.parametrize(
    "environ_vars",
    [
        (
                {"AOC_RUNNER_PROJECT_HOME": False,
                 "AOC_RUNNER_DIR": False,
                 "AOC_RUNNER_AUTH_DIR": False,
                 "AOC_RUNNER_CACHE_DIR": False,
                 "AOC_RUNNER_USERS_DIR": False,
                 }
        ),
        (
                {"AOC_RUNNER_PROJECT_HOME": True,
                 "AOC_RUNNER_DIR": False,
                 "AOC_RUNNER_AUTH_DIR": False,
                 "AOC_RUNNER_CACHE_DIR": False,
                 "AOC_RUNNER_USERS_DIR": False,
                 }
        ),
        (
                {"AOC_RUNNER_PROJECT_HOME": True,
                 "AOC_RUNNER_DIR": True,
                 "AOC_RUNNER_AUTH_DIR": False,
                 "AOC_RUNNER_CACHE_DIR": False,
                 "AOC_RUNNER_USERS_DIR": False,
                 }
        ),
        (
                {"AOC_RUNNER_PROJECT_HOME": False,
                 "AOC_RUNNER_DIR": True,
                 "AOC_RUNNER_AUTH_DIR": False,
                 "AOC_RUNNER_CACHE_DIR": False,
                 "AOC_RUNNER_USERS_DIR": False,
                 }
        ),
        (
                {"AOC_RUNNER_PROJECT_HOME": False,
                 "AOC_RUNNER_DIR": False,
                 "AOC_RUNNER_AUTH_DIR": True,
                 "AOC_RUNNER_CACHE_DIR": True,
                 "AOC_RUNNER_USERS_DIR": True,
                 }
        ),
        (
                {"AOC_RUNNER_PROJECT_HOME": True,
                 "AOC_RUNNER_DIR": False,
                 "AOC_RUNNER_AUTH_DIR": True,
                 "AOC_RUNNER_CACHE_DIR": True,
                 "AOC_RUNNER_USERS_DIR": True,
                 }
        ),
        (
                {"AOC_RUNNER_PROJECT_HOME": False,
                 "AOC_RUNNER_DIR": True,
                 "AOC_RUNNER_AUTH_DIR": True,
                 "AOC_RUNNER_CACHE_DIR": True,
                 "AOC_RUNNER_USERS_DIR": True,
                 }
        ),
        (
                {"AOC_RUNNER_PROJECT_HOME": True,
                 "AOC_RUNNER_DIR": True,
                 "AOC_RUNNER_AUTH_DIR": True,
                 "AOC_RUNNER_CACHE_DIR": True,
                 "AOC_RUNNER_USERS_DIR": True,
                 }
        ),
    ]
)
@pytest.mark.config
def test_runner_home_only(ensure_path_exists, monkeypatch, environ_vars):
    """Test having the AOC_RUNNER_PROJECT_HOME set only"""

    with monkeypatch.context() as patch:
        for key, value in environ_vars.items():
            print(f"Test input key: {key} -> {value}")
            if value:
                patch.setenv(key, key)
            else:
                patch.delenv(key, raising=False)

        # Reload the module with the modified environment variables
        if "aoc_runner.config" in sys.modules:
            reload(sys.modules["aoc_runner.config"])

        from aoc_runner import config

        # Determine the expected project home directory
        if environ_vars.get("AOC_RUNNER_PROJECT_HOME"):
            expect_project_home = Path("AOC_RUNNER_PROJECT_HOME")
        else:
            expect_project_home = Path().cwd().parent
        assert config.AOC_RUNNER_PROJECT_HOME == expect_project_home

        # Determine the expected runner directory
        if environ_vars.get("AOC_RUNNER_DIR"):
            expect_runner_dir = Path("AOC_RUNNER_DIR")
        elif environ_vars.get("AOC_RUNNER_PROJECT_HOME"):
            expect_runner_dir = Path("AOC_RUNNER_PROJECT_HOME") / ".config" / ".aoc_runner"
        else:
            expect_runner_dir = Path("~", ".config", ".aoc_runner").expanduser()
        assert config.AOC_RUNNER_DIR == expect_runner_dir

        # Determine the expected users directory
        if environ_vars.get("AOC_RUNNER_USERS_DIR"):
            expect_users_dir = Path("AOC_RUNNER_USERS_DIR")
        else:
            expect_users_dir = expect_runner_dir / "users"
        assert config.AOC_RUNNER_USERS_DIR == expect_users_dir

        # Determine the expected cache directory
        if environ_vars.get("AOC_RUNNER_CACHE_DIR"):
            expect_cache_dir = Path("AOC_RUNNER_CACHE_DIR")
        else:
            expect_cache_dir = expect_runner_dir / "cache"
        assert config.AOC_RUNNER_CACHE_DIR == expect_cache_dir

        # Determine the expected authentication directory
        if environ_vars.get("AOC_RUNNER_AUTH_DIR"):
            expect_auth_dir = Path("AOC_RUNNER_AUTH_DIR")
        else:
            expect_auth_dir = expect_runner_dir / ".auth"
        assert config.AOC_RUNNER_AUTH_DIR == expect_auth_dir

    # Reload the module into it's original state
    reload(sys.modules["aoc_runner.config"])
