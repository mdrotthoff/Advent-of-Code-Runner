"""Common Advent of Code Runner User fixtures"""

# System libraries
from datetime import datetime
import json
import pickle

# Pytest libraries
import pytest

# Advent of Code Runner libraries
from aoc_runner.user import LOGIN_SOURCES, UserInfo, UserList


class Timeout(BaseException):
    """Simulate a timeout exception"""


INVALID_USER_INFO = [
    {
        "user_name": 1,
        "aoc_id": 1,
        "login_source": LOGIN_SOURCES[0],
        "last_updated": datetime.now(),
        "token": "token",
        "invalid_fields": ["user_name"],
    },
    {
        "user_name": "user_name",
        "aoc_id": "aoc_id",
        "login_source": LOGIN_SOURCES[0],
        "last_updated": datetime.now(),
        "token": "token",
        "invalid_fields": ["aoc_id"],
    },
    {
        "user_name": "user_name",
        "aoc_id": 1.1,
        "login_source": LOGIN_SOURCES[0],
        "last_updated": datetime.now(),
        "token": "token",
        "invalid_fields": ["aoc_id"],
    },
    {
        "user_name": "user_name",
        "aoc_id": -1,
        "login_source": LOGIN_SOURCES[0],
        "last_updated": datetime.now(),
        "token": "token",
        "invalid_fields": ["aoc_id"],
    },
    {
        "user_name": "user_name",
        "aoc_id": 1,
        "login_source": 1,
        "last_updated": datetime.now(),
        "token": "token",
        "invalid_fields": ["login_source"],
    },
    {
        "user_name": "user_name",
        "aoc_id": 1,
        "login_source": "login_source",
        "last_updated": datetime.now(),
        "token": "token",
        "invalid_fields": ["login_source"],
    },
    {
        "user_name": "user_name",
        "aoc_id": 1,
        "login_source": LOGIN_SOURCES[0],
        "last_updated": "last_updated",
        "token": "token",
        "invalid_fields": ["last_updated"],
    },
    {
        "user_name": "user_name",
        "aoc_id": 1,
        "login_source": LOGIN_SOURCES[0],
        "last_updated": datetime.now(),
        "token": 1,
        "invalid_fields": ["token"],
    },
    {
        "user_name": 1,
        "aoc_id": -1,
        "login_source": "login_source",
        "last_updated": "last_updated",
        "token": 1,
        "invalid_fields": ["user_name", "aoc_id", "login_source", "last_updated", "token"],
    },
]


# User data defined
EXPIRED_USERS = [
    {
        "user_name": "expired-user",
        "aoc_id": 1,
        "login_source": "github",
        "last_updated": "2024-01-16T10:12:22.760942",
        "token": "53616c7465645f5f168e2a3588960815d03e3b36461ae4d80d2d4918cbdcba3b9a08a1becf6134815911e83eb748e180ff28aa7abd71e5e28ec15a601603e03b",
    }
]

REAL_USERS = [
    {
        "user_name": "mdrotthoff",
        "aoc_id": 2129276,
        "login_source": "github",
        "last_updated": "2024-01-16T10:12:22.760942",
        "token": "53616c7465645f5f9ae2b7d2af32fc2e3862adb2f08e5a4dc66b594dd1ad760543ad850fd3692a496e07e3993106607dce2a5bfa13aa311d419223b4fd12e564",
    },
    {
        "user_name": "David Rotthoff",
        "aoc_id": 1656784,
        "login_source": "google",
        "last_updated": "2024-01-16T10:12:22.855008",
        "token": "53616c7465645f5f6a517bc02d328a3ecfc5bf02ef49ea4e8a981cfd9bb9f6e51ddbaa6601ce7b79c8ee3405d77dad4016f17640ef249adbb78045b2c6e645e7",
    },
]

VALID_USERS = [
    {
        "user_name": "mdrotthoff",
        "aoc_id": 2129276,
        "login_source": "github",
        "last_updated": "2024-01-16T10:12:22.760942",
        "token": "53616c7465645f5f9ae2b7d2af32fc2e3862adb2f08e5a4dc66b594dd1ad760543ad850fd3692a496e07e3993106607dce2a5bfa13aa311d419223b4fd12e564",
    },
]


@pytest.fixture(params=INVALID_USER_INFO)
def invalid_user_info(request):
    """Return a range of invalid UserInfo data"""

    user_info = request.param
    yield user_info


@pytest.fixture(params=EXPIRED_USERS)
def expired_token(request):
    """Return the Advent of Code user ID and token of expired users"""

    user_info = request.param
    yield user_info.get("token")


@pytest.fixture(params=REAL_USERS)
def real_token(request):
    """Return the Advent of Code user ID and token of valid users"""

    user_info = request.param
    yield user_info.get("aoc_id"), user_info.get("token")


@pytest.fixture(params=VALID_USERS)
def valid_token(request):
    """Return the Advent of Code user ID and token of a valid user"""

    user_info = request.param
    yield user_info.get("aoc_id"), user_info.get("token")


@pytest.fixture
def expired_user():
    """Return a UserInfo structure with valid data"""
    user_info = EXPIRED_USERS[0]
    yield UserInfo(
        user_name=user_info.get("user_name"),
        aoc_id=user_info.get("aoc_id"),
        login_source=user_info.get("login_source"),
        last_updated=user_info.get("last_updated"),
        token=user_info.get("token"),
    )


@pytest.fixture
def expired_user_list():
    """Return a list of UserInfo structures for all expired users"""

    expired_users = [
        UserInfo(
            user_name=user_info.get("user_name"),
            aoc_id=user_info.get("aoc_id"),
            login_source=user_info.get("login_source"),
            last_updated=user_info.get("last_updated"),
            token=user_info.get("token"),
        )
        for user_info in EXPIRED_USERS
    ]
    yield expired_users


@pytest.fixture
def real_user():
    """Return a UserInfo structure with a real user"""
    user_info = REAL_USERS[0]
    yield UserInfo(
        user_name=user_info.get("user_name"),
        aoc_id=user_info.get("aoc_id"),
        login_source=user_info.get("login_source"),
        last_updated=user_info.get("last_updated"),
        token=user_info.get("token"),
    )


@pytest.fixture
def real_users():
    """Return a UserInfo structure with a real user"""

    for user_info in REAL_USERS:
        yield UserInfo(
            user_name=user_info.get("user_name"),
            aoc_id=user_info.get("aoc_id"),
            login_source=user_info.get("login_source"),
            last_updated=user_info.get("last_updated"),
            token=user_info.get("token"),
        )


@pytest.fixture
def valid_user():
    """Return a UserInfo structure with valid data"""
    user_info = VALID_USERS[0]
    yield UserInfo(
        user_name=user_info.get("user_name"),
        aoc_id=user_info.get("aoc_id"),
        login_source=user_info.get("login_source"),
        last_updated=user_info.get("last_updated"),
        token=user_info.get("token"),
    )


@pytest.fixture(params=LOGIN_SOURCES)
def user_data(request):
    """Create a UserInfo object with valid values for each login source"""
    yield UserInfo(
        user_name="test user",
        aoc_id=1,
        login_source=request.param,
        last_updated=datetime.now(),
        token="testtoken",
    )


@pytest.fixture
def make_load_user_settings(request):
    """Create a factory which allows for dynamic loading of token data from file"""

    def make(url: str, token: str, redirect: bool):
        """Load the cached user setting response from the Advent of Code servers"""

        file_path = request.config.rootdir / "tests" / "aoc_runner" / "user" / "data"
        file_name = file_path / f"settings_{token}.pickle"
        print(f"Getting mocked user settings for token {token}")

        if file_name.exists():
            with open(file_name, mode="rb") as file:
                loaded = pickle.load(file)

            return loaded

        file_name = file_path / "settings_no_such_user.pickle"
        if file_name.exists():
            with open(file_name, mode="rb") as file:
                loaded = pickle.load(file)

            return loaded

        raise Timeout

    return make


@pytest.fixture
def user_http_get(user_module_dir_patch, make_load_user_settings, monkeypatch):
    """Monkey patch the http_client.get() to be a local operation"""

    monkeypatch.setattr("aoc_runner.user.http_client.get", make_load_user_settings)


@pytest.fixture
def create_empty_tokens_json():
    """Create an empty tokens.json file"""

    user_list = UserList()
    tokens_file = user_list.tokens_file
    assert tokens_file.exists()


@pytest.fixture
def create_loaded_tokens_json(user_http_get, expired_user, valid_user):
    """Create a loaded tokens.json file"""

    user_list = UserList()
    tokens_file = user_list.tokens_file
    assert tokens_file.exists()

    user_list.add_user(user_info=expired_user)
    user_list.add_user(user_info=valid_user)
    assert tokens_file.exists()


# @pytest.fixture
# def create_default_token_file(user_http_get, valid_token, runner_auth_dir):
#     """Create a default token file"""
#
#     _, token = valid_token
#     token_file = runner_auth_dir / "token"
#     token_file.write_text(token, encoding="utf-8")
#     yield token_file


@pytest.fixture
# def make_default_token_file(user_http_get, valid_token, runner_auth_dir):
def make_default_token_file(runner_auth_dir):
    """Create a default token file"""

    # def make(token, auth_dir=runner_auth_dir):
    def make(token):
        # _, token = valid_token
        token_file = runner_auth_dir / "token"
        token_file.write_text(token, encoding="utf-8")
        return token_file

    return make
