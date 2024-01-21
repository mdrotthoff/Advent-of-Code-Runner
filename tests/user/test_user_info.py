"""Test the Advent of Code Runner UserInfo data class"""

# System libraries
from datetime import datetime
from unittest.mock import patch

# Pytest libraries
import pytest

# Third-party libraries
from pydantic import ValidationError

# Advent of Code Runner libraries
from aoc_runner.user import LOGIN_SOURCES, UserInfo


@pytest.mark.user
@pytest.mark.unit
def test_user_info_invalid_data(invalid_user_info, user_http_get):
    """Test the allowed data types / values for each field of the UserInfo class"""

    with pytest.raises(ValidationError) as excp:
        _ = UserInfo(
            user_name=invalid_user_info.get("user_name"),
            aoc_id=invalid_user_info.get("aoc_id"),
            login_source=invalid_user_info.get("login_source"),
            last_updated=invalid_user_info.get("last_updated"),
            token=invalid_user_info.get("token"),
        )

    invalid_fields = invalid_user_info.get("invalid_fields")
    excp_str = str(excp.value)

    assert excp_str.startswith(f"{len(invalid_fields)} validation error")
    for field in invalid_fields:
        assert field in excp_str


@pytest.mark.parametrize(
    "user_name, aoc_id, last_updated, token",
    [
        ("user_name", 1, datetime.now(), "token"),
    ],
)
@pytest.mark.parametrize("login_source", LOGIN_SOURCES)
@pytest.mark.user
@pytest.mark.integration
def test_user_info_login_source(
        user_name,
        aoc_id,
        login_source,
        last_updated,
        token,
        user_http_get,
):
    """Test that each defined login_source is usable by the UserInfo class"""

    user_info = UserInfo(
        user_name=user_name,
        aoc_id=aoc_id,
        login_source=login_source,
        last_updated=last_updated,
        token=token,
    )
    assert user_info.login_source == login_source
