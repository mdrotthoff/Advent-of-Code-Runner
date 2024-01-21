"""Test the Advent of Code Runner User object"""

# System libraries
from datetime import datetime

# Pytest libraries
import pytest

# Advent of Code Runner libraries
from aoc_runner.exceptions import AocValueError, DeadTokenError
from aoc_runner.user import User


class Timeout(BaseException):
    """Simulate a timeout exception"""


#
# User class __init__ tests
#
@pytest.mark.user
@pytest.mark.unit
def test_user_init(valid_user, user_http_get):  # noqa
    """Test the base __init__ method of the User class with valid input."""

    user = User(user_info=valid_user)
    assert user.user_id == f"{valid_user.login_source}.{valid_user.aoc_id}"
    assert user.user_name == valid_user.user_name
    assert user.aoc_id == valid_user.aoc_id
    assert user.login_source == valid_user.login_source
    assert user.last_updated == valid_user.last_updated
    assert user.token == valid_user.token
    assert user.user_info == valid_user


@pytest.mark.user
@pytest.mark.unit
def test_user_init_bad_parameter(valid_user, user_http_get):
    """Test the base __init__ method of the User class with bad input."""

    with pytest.raises(AocValueError) as excp:
        user = User(user_info=valid_user.token)

    excp_msg = str(excp.value)
    assert excp_msg.startswith("User_info parameter must be of UserInfo type not")


#
#  Test property getters
#
@pytest.mark.user
@pytest.mark.unit
def test_user_getter_aoc_id(user_http_get, runner_users_dir, valid_user):
    """Test the User.aoc_id property returns the expected value"""

    user = User(user_info=valid_user)
    assert user.aoc_id == valid_user.aoc_id


@pytest.mark.user
@pytest.mark.unit
def test_user_getter_last_updated(user_http_get, runner_users_dir, valid_user):
    """Test the User.last_updated property returns the expected value"""

    user = User(user_info=valid_user)
    assert user.last_updated == valid_user.last_updated


@pytest.mark.user
@pytest.mark.unit
def test_user_getter_login_source(user_http_get, runner_users_dir, valid_user):
    """Test the User.login_source property returns the expected value"""

    user = User(user_info=valid_user)
    assert user.login_source == valid_user.login_source


@pytest.mark.user
@pytest.mark.unit
def test_user_getter_memo(user_http_get, runner_users_dir, valid_user):
    """Test the User.memo property returns the expected value"""

    user = User(user_info=valid_user)
    assert user.memo.parent == runner_users_dir


@pytest.mark.user
@pytest.mark.unit
def test_user_getter_token(user_http_get, runner_users_dir, valid_user):
    """Test the User.token property returns the expected value"""

    user = User(user_info=valid_user)
    assert user.token == valid_user.token


@pytest.mark.user
@pytest.mark.unit
def test_user_getter_user_id(user_http_get, runner_users_dir, valid_user):
    """Test the User.user_id property returns the expected value"""

    user = User(user_info=valid_user)
    assert user.user_id == f"{valid_user.login_source}.{valid_user.aoc_id}"


#
#  Test property setters
#
@pytest.mark.user
@pytest.mark.unit
def test_user_setter_last_updated(valid_user, user_http_get):
    """Test the User.token setter method of the User class."""

    last_updated = datetime.now()
    user = User(user_info=valid_user)
    user.last_updated = last_updated
    assert user.last_updated == last_updated


@pytest.mark.user
@pytest.mark.unit
def test_user_setter_last_updated_bad_parameter(valid_user, user_http_get):
    """Test the user.token setter method of the User class."""

    user = User(user_info=valid_user)
    with pytest.raises(AocValueError) as excp:
        user.last_updated = valid_user

    excp_str = str(excp.value)
    assert excp_str.startswith("token parameter must be of str type not")


@pytest.mark.user
@pytest.mark.unit
def test_user_setter_token(valid_user, user_http_get):
    """Test the user.token setter method of the User class."""

    token = f"Updated-token-{datetime.now().isoformat()}"
    last_updated = valid_user.last_updated
    user = User(user_info=valid_user)
    user.token = token
    assert user.token == token
    assert user.last_updated > last_updated


@pytest.mark.user
@pytest.mark.unit
def test_user_setter_token_bad_parameter(valid_user, user_http_get):
    """Test the user.token setter method of the User class."""

    user = User(user_info=valid_user)
    with pytest.raises(AocValueError) as excp:
        user.token = valid_user

    excp_str = str(excp.value)
    assert excp_str.startswith("token parameter must be of str type not")


#
#  Test from_token class method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_from_token(real_token, user_http_get):
    """Test the user.from_token method with valid Advent of Code users"""

    aoc_id, token = real_token
    user = User.from_token(token=token)
    assert user.aoc_id == aoc_id


@pytest.mark.user
@pytest.mark.unit
def test_user_from_token_expired(expired_token, user_http_get):
    """Test the user.from_token method with expired Advent of Code users"""

    token = expired_token
    with pytest.raises(DeadTokenError) as excp:
        _ = User.from_token(token=token)

    excp_str = str(excp.value)
    assert excp_str.startswith("The auth token ...")


@pytest.mark.user
@pytest.mark.unit
def test_user_from_token_bad_parameter(real_token, user_http_get):
    """Test the user.from_token method with expired Advent of Code users"""

    # aoc_id, token = real_token

    with pytest.raises(AocValueError) as excp:
        user = User.from_token(token=real_token)

    excp_str = str(excp.value)
    assert excp_str.startswith("token parameter must be of str type not")
