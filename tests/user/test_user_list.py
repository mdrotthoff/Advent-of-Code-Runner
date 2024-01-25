"""Test the Advent of Code Runner User object"""

# System libraries
from os import environ
from time import sleep

# Pytest libraries
import pytest

# Advent of Code Runner libraries
from aoc_runner.exceptions import (
    NoSuchUser,
    TokenFileChanged,
    UnknownLoginSource,
    UserAlreadyExists,
)
from aoc_runner.user import UserList


@pytest.mark.debug
def test_show_environment():
    """Show the current environment variables"""

    for key in sorted(environ.keys()):
        print(f"\t{key}: {environ[key]}")


#
#  Test __init__ method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_init_new_no_file(
    user_http_get,
):
    """Test the UserList class initialization where the file did not
    exist and there is no default token available either as a file
    or in the environment variables
    """

    tokens_file = UserList().tokens_file
    if tokens_file.exists():
        tokens_file.unlink()

    assert not tokens_file.exists()
    user_list = UserList()
    assert tokens_file.exists()
    assert user_list.default_user is None


@pytest.mark.user
@pytest.mark.unit
def test_user_list_init_new_no_file_default_token_file(
    user_http_get,
    make_default_token_file,
    valid_user,
):
    """Test the UserList class initialization where the file did not
    exist and there is a default token available as a file
    """

    token_file = make_default_token_file(token=valid_user.token)
    assert token_file.exists()

    user_list = UserList()
    tokens_file = UserList().tokens_file
    assert not token_file.exists()
    assert tokens_file.exists()
    assert user_list.default_user is not None


@pytest.mark.user
@pytest.mark.unit
def test_user_list_init_existing(
    user_http_get,
    expired_user,
    create_loaded_tokens_json,
):
    """Test the UserList class initialization where the file does
    exist and there is no token available in the environment variables
    but a default token file exists
    """

    user_list = UserList()
    tokens_file = user_list.tokens_file
    assert tokens_file.exists()
    assert user_list._default_user is not None
    assert len(user_list._users) > 0


#
#  Test _get_default_token method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_default_token_no_default(
    user_http_get,
    expired_user,
):
    """Test the UserList class _get_default_token where there is no
    default token available either as a file or in the environment
    variables
    """

    user_list = UserList()
    user_list._get_default_token()
    assert user_list._default_user is None


@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_default_token_file_token(
    user_http_get,
    valid_user,
    make_default_token_file,
):
    """Test the UserList class _get_default_token where there is a
    default token available as a file but not in the environment
    variables
    """

    user_list = UserList()
    assert user_list._default_user is None

    token_file = make_default_token_file(token=valid_user.token)
    assert token_file.exists()

    user_list._get_default_token()
    assert user_list._default_user is not None


@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_default_token_session_token(
    user_http_get,
    expired_user,
    valid_user,
    monkeypatch,
):
    """Test the UserList class _get_default_token where there is a
    default token available in the environment variables but not as a file
    """

    user_list = UserList()
    assert user_list._default_user is None
    monkeypatch.setenv("AOC_RUNNER_SESSION", valid_user.token)

    user_list._get_default_token()
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id


@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_default_token_both(
    user_http_get,
    expired_user,
    valid_user,
    make_default_token_file,
    monkeypatch,
):
    """Test the UserList class _get_default_token where there is a
    default token available as both an environment variables and in
    a file.  Token from the environment variable should be used.
    """

    user_list = UserList()
    assert user_list._default_user is None

    token_file = make_default_token_file(token=expired_user.token)
    assert token_file.exists()
    monkeypatch.setenv("AOC_RUNNER_SESSION", valid_user.token)

    user_list._get_default_token()
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id


@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_default_token_user_exists(
    user_http_get,
    valid_user,
    monkeypatch,
):
    """Test the UserList class _get_default_token where there is a
    default token available in the environment variables.  The default
    user does exists in UserList
    """

    user_list = UserList()
    user_list.add_user(user_info=valid_user)
    assert user_list._default_user is not None

    monkeypatch.setenv("AOC_RUNNER_SESSION", valid_user.token)
    initial_default_user = user_list._default_user

    user_list._get_default_token()
    assert user_list._default_user is not None
    assert user_list._default_user == initial_default_user


@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_default_token_user_exists_different_token(
    user_http_get,
    valid_user,
    monkeypatch,
):
    """Test the UserList class _get_default_token where there is a
    default token available in the environment variables.  The default
    user does exists in UserList
    """

    old_user = valid_user.model_copy()
    old_user.token = "Test token"
    user_list = UserList()
    user_list.add_user(user_info=old_user)
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].token == old_user.token
    assert not old_user.token == valid_user.token

    monkeypatch.setenv("AOC_RUNNER_SESSION", valid_user.token)
    initial_default_user = user_list._default_user

    user_list._get_default_token()
    assert user_list._default_user is not None
    assert user_list._default_user == initial_default_user
    assert user_list._users[user_list._default_user].token == valid_user.token


@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_default_token_no_exists(
    user_http_get,
    expired_user,
    valid_user,
    monkeypatch,
):
    """Test the UserList class _get_default_token where there is a
    default token available in the environment variables.  The default
    user does NOT exist in UserList
    """

    user_list = UserList()
    user_list.add_user(user_info=expired_user)
    assert user_list._default_user is not None

    monkeypatch.setenv("AOC_RUNNER_SESSION", valid_user.token)
    initial_default_user = user_list._default_user
    assert len(user_list._users) == 1

    user_list._get_default_token()
    assert user_list._default_user is not None
    assert not user_list._default_user == initial_default_user
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id
    assert len(user_list._users) == 2


#
#  Test _get_token_owner method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_token_owner_no_user(
    user_http_get,
    valid_user,
):
    """Test the UserList._get_token_owner returns none when the token is
    not defined in tokens.json
    """

    user_list = UserList()
    result = user_list._get_token_owner(token=valid_user.token)
    assert result is None


@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_token_owner_user_exists(
    user_http_get,
    valid_user,
):
    """Test the UserList._get_token_owner returns the correct user ID when
    the token is defined in tokens.json
    """

    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    user_list = UserList()
    assert user_list.default_user is None

    user_list.add_user(user_info=valid_user, force=False)
    assert user_list.default_user == user_id

    result = user_list._get_token_owner(token=valid_user.token)
    assert result == user_id


#
#  Test _load method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_load_no_file(
    user_http_get,
):
    """Test the UserList.load method when no file is available"""

    user_list = UserList()
    tokens_file = user_list.tokens_file
    if tokens_file.exists():
        tokens_file.unlink()

    assert not tokens_file.exists()
    user_list._load()
    assert user_list._default_user is None
    assert len(user_list._users) == 0


@pytest.mark.user
@pytest.mark.unit
def test_user_list_load_no_file_with_users(
    user_http_get,
    create_loaded_tokens_json,
):
    """Test the UserList.load method when no file is available but data
    already exists in the class
    """

    user_list = UserList()
    tokens_file = user_list.tokens_file
    if tokens_file.exists():
        tokens_file.unlink()

    assert not tokens_file.exists()
    user_list._load()
    assert user_list._default_user is not None
    assert len(user_list._users) > 0


@pytest.mark.user
@pytest.mark.unit
def test_user_list_load_file_no_users(
    user_http_get,
    create_empty_tokens_json,
):
    """Test the UserList.load method when a file is available but no
    users are defined"""

    user_list = UserList()
    user_list._load()
    assert user_list._default_user is None
    assert len(user_list._users) == 0


@pytest.mark.user
@pytest.mark.unit
def test_user_list_load_file_with_users(
    user_http_get,
    create_loaded_tokens_json,
):
    """Test the UserList.load method when a file is available that has
    users are defined"""

    user_list = UserList()
    user_list._load()
    assert user_list._default_user is not None
    assert len(user_list._users) > 0


#
#  Test _save method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_save_no_file(
    user_http_get,
):
    """Test the UserList.save() method when no file exists"""

    user_list = UserList()
    assert user_list._default_user is None
    assert len(user_list._users) == 0
    tokens_file = user_list.tokens_file

    if tokens_file.exists():
        tokens_file.unlink()

    user_list._save()
    assert tokens_file.exists()


@pytest.mark.user
@pytest.mark.unit
def test_user_list_save_file_exists(
    user_http_get,
):
    """Test the UserList.save() method when a file already exists"""

    user_list = UserList()
    assert user_list._default_user is None
    assert len(user_list._users) == 0
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime

    sleep(0.01)
    user_list._save()
    assert tokens_file.exists()
    assert tokens_file.stat().st_mtime > modified_time


@pytest.mark.user
@pytest.mark.unit
def test_user_list_save_file_updated(
    user_http_get,
):
    """Test the UserList.save() method when a file already exists
    but has been updated since it was loaded"""

    user_list = UserList()
    assert user_list._default_user is None
    assert len(user_list._users) == 0
    tokens_file = user_list.tokens_file

    sleep(0.01)
    tokens_file.touch()
    modified_time = tokens_file.stat().st_mtime

    with pytest.raises(TokenFileChanged) as excp:
        user_list._save()

    assert tokens_file.exists()
    assert tokens_file.stat().st_mtime == modified_time


#
#  Test add_token method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_add_token_no_user(
    user_http_get,
    valid_user,
):
    """Test the UserList.add_token() method where the token does not exist"""

    user_list = UserList()
    user_list.add_token(token=valid_user.token)
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id


@pytest.mark.user
@pytest.mark.unit
def test_user_list_add_token_user_exists(
    user_http_get,
    valid_user,
):
    """Test the UserList.add_token() method where the token does exist"""

    user_list = UserList()
    user_list.add_token(token=valid_user.token)
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id

    user_list = UserList()
    user_list.add_token(token=valid_user.token)
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id


@pytest.mark.user
@pytest.mark.unit
def test_user_list_add_token_user_exists_different_token(
    user_http_get,
    valid_user,
):
    """Test the UserList.add_token() method where the token does exist"""

    old_user = valid_user.model_copy()
    old_user.token = "Test token"
    user_list = UserList()
    user_list.add_user(user_info=old_user)
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id

    user_list = UserList()

    with pytest.raises(UserAlreadyExists) as excp:
        user_list.add_token(token=valid_user.token, force=False)

    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == old_user.aoc_id
    assert user_list._users[user_list._default_user].token == old_user.token


@pytest.mark.user
@pytest.mark.unit
def test_user_list_add_token_user_exists_different_token_forced(
    user_http_get,
    valid_user,
):
    """Test the UserList.add_token() method where the token does exist"""

    old_user = valid_user.model_copy()
    old_user.token = "Test token"
    user_list = UserList()
    user_list.add_user(user_info=old_user)
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id

    user_list = UserList()
    user_list.add_token(token=valid_user.token, force=True)
    assert user_list._default_user is not None
    assert user_list._users[user_list._default_user].aoc_id == valid_user.aoc_id


#
#  Test add_user method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_add_user(
    user_http_get,
    valid_user,
):
    """Test the UserList.add_user adds the defined user to an empty
    user list and sets it as the default token
    """

    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    user_list = UserList()
    assert user_list.default_user is None

    user_list.add_user(user_info=valid_user, force=False)
    result = user_list._get_token_owner(valid_user.token)
    assert user_list.default_user == user_id
    assert result == f"{valid_user.login_source}.{valid_user.aoc_id}"


@pytest.mark.user
@pytest.mark.unit
def test_user_list_add_user_exists_not_forced(
    user_http_get,
    valid_user,
):
    """Test the UserList.add_user raises an exception when the user to be
    added already exists in the user list.  Exception UserAlreadyExists
    should be raised.
    """

    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    user_list = UserList()
    assert user_list.default_user is None

    user_list.add_user(user_info=valid_user, force=False)
    assert user_list.default_user == user_id

    with pytest.raises(UserAlreadyExists) as excp:
        user_list.add_user(user_info=valid_user, force=False)

    excp_msg = str(excp.value)
    assert excp_msg.startswith(f"User {user_id} already exists in")
    assert user_list.default_user == user_id


@pytest.mark.user
@pytest.mark.unit
def test_user_list_add_user_exists_forced(
    user_http_get,
    valid_user,
):
    """Test the UserList.add_user when the user already exists and the
    force option is set.  No exception should be raised.
    """

    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    user_list = UserList()
    assert user_list.default_user is None

    user_list.add_user(user_info=valid_user, force=False)
    assert user_list.default_user == user_id

    user_list.add_user(user_info=valid_user, force=True)
    assert user_list.default_user == user_id


@pytest.mark.user
@pytest.mark.unit
def test_user_list_add_user_invalid_login_source(
    user_http_get,
    valid_user,
):
    """Test the UserList.add_user adds the defined user to an empty
    user list and sets it as the default token
    """

    valid_user.login_source = "test_login"
    user_list = UserList()
    assert user_list.default_user is None

    with pytest.raises(UnknownLoginSource) as excp:
        user_list.add_user(user_info=valid_user, force=False)

    excp_msg = str(excp.value)
    assert excp_msg.startswith("Unknown login source of")
    assert user_list.default_user is None


#
#  Test get_users method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_users_no_users(
    user_http_get,
    valid_user,
):
    """Test the UserList.get_users returns an empty dictionary if there
    not any users defined
    """

    # user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    user_list = UserList()
    assert user_list.default_user is None

    users = user_list.get_users()
    assert len(users) == 0


@pytest.mark.user
@pytest.mark.unit
def test_user_list_get_users_defined_users(
    user_http_get,
    valid_user,
):
    """Test the UserList.get_users returns an dictionary with user(s)
    defined that is as long as the number of users defined.
    """

    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    user_list = UserList()
    assert user_list.default_user is None

    user_list.add_user(user_info=valid_user, force=False)
    assert user_list.default_user == user_id

    users = user_list.get_users()
    assert len(users) == 1


#
#  Test remove_user method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_remove_user_no_user(
    user_http_get,
    valid_user,
):
    """Test the UserList.remove_user() method where the user does not exist.
    Tokens file should not be updated
    """

    user_list = UserList()
    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime

    user_list.remove_user(user_id=user_id)
    assert user_list._default_user is None
    assert tokens_file.stat().st_mtime == modified_time


@pytest.mark.user
@pytest.mark.unit
def test_user_list_remove_user_single_user(
    user_http_get,
    valid_user,
):
    """Test the UserList.remove_user() method where the user exists
    as the only user. Tokens file should be updated
    """

    user_list = UserList()
    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    user_list.add_user(user_info=valid_user)
    assert user_list._default_user == user_id

    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime

    sleep(0.01)
    user_list.remove_user(user_id=user_id)
    assert user_list._default_user is None
    assert tokens_file.stat().st_mtime > modified_time


@pytest.mark.user
@pytest.mark.unit
def test_user_list_remove_user_multi_user(
    user_http_get,
    valid_user,
    expired_user,
):
    """Test the UserList.remove_user() method where multiple users exist.  User
    removed is the default user.  Tokens file should be updated
    """

    user_list = UserList()
    expired_user_id = f"{expired_user.login_source}.{expired_user.aoc_id}"
    valid_user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    user_list.add_user(user_info=expired_user)
    user_list.add_user(user_info=valid_user)
    assert user_list._default_user is not None
    assert user_list._default_user == expired_user_id

    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime

    sleep(0.01)
    user_list.remove_user(user_id=expired_user_id)
    assert user_list._default_user is not None
    assert user_list._default_user == valid_user_id
    assert tokens_file.stat().st_mtime > modified_time


#
#  Test set_default_token method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_set_default_token_no_user(
    user_http_get,
    valid_user,
):
    """Test the UserList.set_default_token() method where the user does not exist.
    Exception NoSuchUser should be raised
    """

    user_list = UserList()
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime

    with pytest.raises(NoSuchUser) as excp:
        user_list.set_default_token(token=valid_user.token)

    excp_msg = str(excp.value)
    assert excp_msg.startswith("No user found with token")
    assert tokens_file.stat().st_mtime == modified_time


@pytest.mark.user
@pytest.mark.unit
def test_user_list_set_default_token_user_is_default(
    user_http_get,
    valid_user,
):
    """Test the UserList.set_default_token() method where the user is
    already the default user.  Default user should not change and file
    should not be saved.
    """

    user_list = UserList()
    user_list.add_user(user_info=valid_user)
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime
    default_user = user_list._default_user

    sleep(0.01)
    user_list.set_default_token(token=valid_user.token)
    assert tokens_file.stat().st_mtime == modified_time
    assert user_list._default_user == default_user


@pytest.mark.user
@pytest.mark.unit
def test_user_list_set_default_token_user_is_not_default(
    user_http_get,
    expired_user,
    valid_user,
):
    """Test the UserList.set_default_token() method where the user does not exist.
    Default user should not change and file should not be saved.
    """

    user_list = UserList()
    user_list.add_user(user_info=expired_user)
    # default_user = user_list._default_user
    user_list.add_user(user_info=valid_user)
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime
    valid_user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"

    sleep(0.01)
    user_list.set_default_token(token=valid_user.token)
    assert tokens_file.stat().st_mtime > modified_time
    assert user_list._default_user == valid_user_id


#
#  Test set_default_user method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_set_default_user_no_user(
    user_http_get,
    valid_user,
):
    """Test the UserList.set_default_user() method where the user does not exist.
    Exception NoSuchUser should be raised
    """

    user_list = UserList()
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime
    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"

    with pytest.raises(NoSuchUser) as excp:
        user_list.set_default_user(user_id=user_id)

    excp_msg = str(excp.value)
    assert excp_msg.startswith("No user found with id")
    assert tokens_file.stat().st_mtime == modified_time


@pytest.mark.user
@pytest.mark.unit
def test_user_list_set_default_user_user_is_default(
    user_http_get,
    valid_user,
):
    """Test the UserList.set_default_user() method where the user is
    already the default user.  Default user should not change and file
    should not be saved.
    """

    user_list = UserList()
    user_list.add_user(user_info=valid_user)
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime
    default_user = user_list._default_user

    sleep(0.01)
    user_list.set_default_user(user_id=default_user)
    assert tokens_file.stat().st_mtime == modified_time
    assert user_list._default_user == default_user


@pytest.mark.user
@pytest.mark.unit
def test_user_list_set_default_user_user_is_not_default(
    user_http_get,
    expired_user,
    valid_user,
):
    """Test the UserList.set_default_user() method where the user does not exist.
    Default user should not change and file should not be saved.
    """

    user_list = UserList()
    user_list.add_user(user_info=expired_user)
    user_list.add_user(user_info=valid_user)
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime
    valid_user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"

    sleep(0.01)
    user_list.set_default_user(user_id=valid_user_id)
    assert tokens_file.stat().st_mtime > modified_time
    assert user_list._default_user == valid_user_id


#
#  Test update_token method
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_update_token_no_user(
    user_http_get,
    valid_user,
):
    """Test the UserList.update_token() method where the user does not exist.
    Exception NoSuchUser should be raised
    """

    user_list = UserList()
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime
    user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"

    with pytest.raises(NoSuchUser) as excp:
        user_list.update_token(user_id=user_id, token=valid_user.token)

    excp_msg = str(excp.value)
    assert excp_msg.startswith("No user found with id")
    assert tokens_file.stat().st_mtime == modified_time


@pytest.mark.user
@pytest.mark.unit
def test_user_list_update_token_current_token(
    user_http_get,
    valid_user,
):
    """Test the UserList.set_default_user() method where the user exists
    amd the token matches the new value.  The user token should not change
    and file should not be saved.
    """

    user_list = UserList()
    user_list.add_user(user_info=valid_user)
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime
    default_user = user_list._default_user

    sleep(0.01)
    assert user_list._users[user_list._default_user].token == valid_user.token
    user_list.update_token(user_id=default_user, token=valid_user.token)
    assert tokens_file.stat().st_mtime == modified_time
    assert user_list._default_user == default_user
    assert user_list._users[user_list._default_user].token == valid_user.token


@pytest.mark.user
@pytest.mark.unit
def test_user_list_update_token_different_token(
    user_http_get,
    expired_user,
    valid_user,
):
    """Test the UserList.update_token() method where the user exists with a
    different token.  The user token should be change and file should be
    saved.
    """

    user_list = UserList()
    user_list.add_user(user_info=valid_user)
    tokens_file = user_list.tokens_file
    modified_time = tokens_file.stat().st_mtime
    valid_user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    last_updated = user_list._users[user_list._default_user].last_updated
    assert user_list._default_user == valid_user_id

    sleep(0.01)
    user_list.update_token(user_id=valid_user_id, token=expired_user.token)
    assert tokens_file.stat().st_mtime > modified_time
    assert user_list._default_user == valid_user_id
    assert user_list._users[user_list._default_user].token == expired_user.token
    assert user_list._users[user_list._default_user].last_updated > last_updated


#
#  Test property getters
#
@pytest.mark.user
@pytest.mark.unit
def test_user_list_getter_default_token_file(
    user_http_get,
    runner_auth_dir,
):
    """Test the UserList.default_token_file() property returns the
    expected value.
    """

    user_list = UserList()
    default_token_file = user_list.default_token_file
    assert default_token_file == runner_auth_dir / "token"


@pytest.mark.user
@pytest.mark.unit
def test_user_list_getter_get_default_user_no_user(
    user_http_get,
    runner_auth_dir,
):
    """Test the UserList.get_default_user() property returns None when
    there are no users.
    """

    user_list = UserList()
    default_user = user_list.default_user
    assert default_user is None


@pytest.mark.user
@pytest.mark.unit
def test_user_list_getter_get_default_user_valid_user(
    user_http_get,
    runner_auth_dir,
    valid_user,
):
    """Test the UserList.get_default_user() property returns the current
    default user when there are users.
    """

    user_list = UserList()
    user_list.add_user(user_info=valid_user)
    valid_user_id = f"{valid_user.login_source}.{valid_user.aoc_id}"
    default_user = user_list.default_user
    assert default_user == valid_user_id


@pytest.mark.user
@pytest.mark.unit
def test_user_list_getter_tokens_file(
    user_http_get,
    runner_auth_dir,
):
    """Test the UserList.tokens_file() property returns the
    expected value.
    """

    user_list = UserList()
    tokens_file = user_list.tokens_file
    assert tokens_file == runner_auth_dir / "tokens.json"
