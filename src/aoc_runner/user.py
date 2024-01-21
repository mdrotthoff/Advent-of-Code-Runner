"""Advent of Code Runner user model"""

# System libraries
from copy import deepcopy
from datetime import datetime
import json
import logging
from os import getenv
from pathlib import Path

# Third-party libraries
from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    field_validator,
)

# Advent of Code Runner libraries
from .config import (
    AOC_DOMAIN,
    AOC_RUNNER_AUTH_DIR,
    AOC_RUNNER_USERS_DIR,
)
from .exceptions import (
    AocValueError,
    DeadTokenError,
    # MissingSessionToken,
    NoSuchUser,
    TokenFileChanged,
    UnknownLoginSource,
    UserAlreadyExists,
)
from .httpclient import http_client
from .utils import (
    # color,
    # colored,
    get_soup,
)

log = logging.getLogger(__name__)
LOGIN_SOURCES = ["github", "google", "twitter", "reddit"]


# @dataclass
class UserInfo(BaseModel):
    """Define the data captured about a specific Advent of Code user"""
    # TODO:  Add a property of user_id
    user_name: str
    aoc_id: int = Field(gt=0)
    login_source: str
    last_updated: datetime
    token: str

    @field_serializer("last_updated")
    def serialize_last_updated(self, last_updated: datetime) -> str:
        """Serialize the last updated as a string"""
        return last_updated.isoformat()

    @field_validator("login_source")
    @classmethod
    def login_source_must_be_defined(cls, login_source: str):
        """Ensure the specified login source is defined"""
        if login_source not in LOGIN_SOURCES:
            raise ValueError("source is not defined")
        return login_source


class User:
    """This is the main user object used to manage the connection to
    the Advent of Code server.
    """

    def __init__(self, user_info: UserInfo) -> None:
        """Initialize the user object from the provided Advent of
        Code session token
        """

        if not isinstance(user_info, UserInfo):
            log.error("User_info parameter must be of UserInfo type not %s", type(user_info))
            raise AocValueError(f"User_info parameter must be of UserInfo type not {type(user_info)}")

        self._user_info: UserInfo = user_info
        log.debug("Class User successfully initialized")

    @classmethod
    def from_token(cls, token: str) -> "User":
        """Find the owner of the specified token. Raises DeadTokenError if the token is
        expired or invalid. Returns a User object
        """
        """Set the user's token"""
        if not isinstance(token, str):
            log.error("token parameter must be of str type not %s", type(token))
            raise AocValueError(f"token parameter must be of str type not {type(token)}")

        url = f"{AOC_DOMAIN}/settings"
        response = http_client.get(url, token=token, redirect=False)
        if response.status != 200:
            # bad tokens will 302 redirect to main page
            log.info("Session %s is dead - status_code=%s", token, response.status)
            raise DeadTokenError(f"The auth token ...{token[-4:]} is dead")

        soup = get_soup(response.data)
        login_source = "unknown"
        user_name = "unknown"
        userid = soup.code.text.split("-")[1]
        for span in soup.find_all("span"):
            if span.text.startswith("Link to "):
                login_source = span.text[8:]
                login_source = login_source.replace("https://twitter.com/", "twitter/")
                login_source = login_source.replace("https://github.com/", "github/")
                login_source = login_source.replace("https://www.reddit.com/u/", "reddit/")
                login_source, sep, user_name = login_source.partition("/")
                if not sep:
                    log.warning("problem in parsing %s", span.text)
                    login_source = user_name = "unknown"
                log.debug("found %r", span.text)
            elif span.img is not None:
                if "googleusercontent.com" in span.img.attrs.get("src", ""):
                    log.debug("found google user content img, getting google username")
                    login_source = "google"
                    user_name = span.text
                    break

        user_info = UserInfo(
            user_name=user_name,
            aoc_id=int(userid),
            login_source=login_source,
            last_updated=datetime.now(),
            token=token,
        )

        user = User(user_info=user_info)
        log.debug(
            "Created user %s.%s for token %s",
            user._user_info.login_source,
            user._user_info.aoc_id,
            token,
        )
        return user

    @property
    def aoc_id(self) -> int:
        """Return the user's Advent of Code ID"""
        return self._user_info.aoc_id

    @property
    def last_updated(self) -> datetime:
        """Return the user's login source"""
        return self._user_info.last_updated

    @last_updated.setter
    def last_updated(self, last_updated: datetime) -> None:
        """Update the last updated for the user"""
        if not isinstance(last_updated, datetime):
            log.error("token parameter must be of str type not %s", type(last_updated))
            raise AocValueError(f"token parameter must be of str type not {type(last_updated)}")

        self._user_info.last_updated = last_updated

    @property
    def login_source(self) -> str:
        """Return the user's login source"""
        return self._user_info.login_source

    @property
    def memo(self) -> Path:
        """Return the user's indiviaual cache directory"""
        return AOC_RUNNER_USERS_DIR / self.user_id

    @property
    def token(self) -> str:
        """Return the user's token"""
        return self._user_info.token

    @token.setter
    def token(self, token: str) -> None:
        """Set the user's token"""
        if not isinstance(token, str):
            log.error("token parameter must be of str type not %s", type(token))
            raise AocValueError(f"token parameter must be of str type not {type(token)}")

        self._user_info.token = token
        self._user_info.last_updated = datetime.now()

    @property
    def user_id(self) -> str:
        """Return the user ID associated with the user"""
        return f"{self._user_info.login_source}.{self._user_info.aoc_id}"

    @property
    def user_name(self) -> str:
        """Return the username associated with the user"""
        return self._user_info.user_name

    @property
    def user_info(self) -> UserInfo:
        """Return the user information associated with the user"""
        user_info = self._user_info.model_copy()
        return user_info


class UserList:
    """Managed the list of Advent of Code users known"""

    def __init__(self) -> None:
        """Initialize the class from the source file"""
        self._users: dict[str, User] = {}
        self._default_user: str | None = None
        self._last_modified: float = 0

        # Load the currently save state
        self._load()
        # Look for a defined default token
        self._get_default_token()
        # Save the current state
        self._save()
        # Remove the default default token file
        if self.default_token_file.exists():
            self.default_token_file.unlink()
            log.debug("Removed default token file %s", self.default_token_file)
        log.debug("Class UserList successfully initialized")

    def _get_default_token(self) -> None:
        """Discover user's token from the environment or file. This default user is
        used whenever a token or user id was otherwise unspecified.
        """
        # Import your session id from environment variable AOC_RUNNER_SESSION
        token = getenv("AOC_RUNNER_SESSION")
        if token:
            log.debug("Token loaded from environment variable")

        # Or save it in a plaintext file at AOC_RUNNER_AUTH_DIR/token
        elif self.default_token_file.exists():
            token = (AOC_RUNNER_AUTH_DIR / "token").read_text(encoding="utf-8").split()[0]
            log.debug("Token loaded from default token file")

        # If a default token was found, make sure it is in the list of
        # managed users and set it as the default
        if token:
            log.debug("Default token %s found", token)
            user_id = self._get_token_owner(token=token)
            if user_id is None:
                user = User.from_token(token=token)
                user_id = f"{user.login_source}.{user.aoc_id}"
                if user_id not in self._users:
                    log.debug("Adding new user %s to %s", user_id, self.tokens_file)
                    self._users[user_id] = user
                else:
                    log.debug("Updated token for existing user %s to %s", user_id, token)
                    self._users[user_id].token = token

                self._default_user = user_id
            else:
                self._default_user = user_id
            log.debug("Default user set to %s", user_id)
        else:
            log.info("No default token file found")

    def _get_token_owner(self, token: str) -> str | None:
        """Get the user ID associated with the supplied token"""
        for user_id, user_info in self._users.items():
            if user_info.token == token:
                log.debug("Found token %s owned by %s", token, user_id)
                return user_id

        log.info("No owner found for token %s", token)
        return None

    def _load(self) -> None:
        """Load the current known users from the source file"""
        if self.tokens_file.exists():
            load_state = json.loads(self.tokens_file.read_text(encoding="utf-8"))
            self._last_modified = self.tokens_file.stat().st_mtime
            self._users = {}
            self._default_user = load_state["default_user"]

            for user_data in load_state["users"]:
                user = User(user_info=UserInfo.model_validate(user_data))
                user_id = f"{user.login_source}.{user.aoc_id}"
                self._users[user_id] = user
            log.debug("Loaded user list from %s", self.tokens_file)
        else:
            log.debug("User list not found at %s", self.tokens_file)

    def _save(self) -> None:
        """Save the current state of the User List to the tokens.json file"""
        save_state = {
            "default_user": self._default_user,
            "users": [user.user_info.model_dump() for user in self._users.values()],
        }

        if (
            self.tokens_file.exists()
            and self._last_modified != self.tokens_file.stat().st_mtime
        ):
            log.error("Tokens file %s was modified since it was last read", self.tokens_file)
            raise TokenFileChanged

        self.tokens_file.write_text(json.dumps(save_state, indent=2))
        self._last_modified = self.tokens_file.stat().st_mtime
        log.debug("Token file %s was successfully saved", self.tokens_file)

    def add_token(self, token: str, force: bool = False) -> None:
        """Add a token to the list of managed users"""
        user = User.from_token(token=token)
        user_id = f"{user.login_source}.{user.aoc_id}"
        if user_id in self._users:
            if self._users[user_id].token == token:
                log.debug(
                    "User %s with token %s already exists in %s",
                    user_id,
                    token,
                    self.tokens_file,
                )
                return
            if not force:
                log.error(
                    "User %s with a different token id already exists in %s",
                    user_id,
                    self.tokens_file,
                )
                raise UserAlreadyExists(f"User {user_id} already exists in tokens.json")

        self._users[user_id] = user
        # self._users[user_id].last_updated = str(datetime.now())
        self._users[user_id].last_updated = datetime.now()
        log.debug(
            "User %s with token %s added to %s",
            user_id,
            token,
            self.tokens_file,
        )

        if self._default_user is None:
            self._default_user = user_id
            log.debug("User %s set as the default user ID", user_id)

        self._save()

    def add_user(self, user_info: UserInfo, force: bool = False) -> None:
        """Add a user to the list of managed users"""
        if user_info.login_source.lower() not in LOGIN_SOURCES:
            log.error("Unknown login source %s", user_info.login_source)
            raise UnknownLoginSource(f"Unknown login source of {user_info.login_source}")

        user_id = f"{user_info.login_source}.{user_info.aoc_id}"
        if user_id in self._users and not force:
            log.error("User %s already exists in %s", user_id, self.tokens_file)
            raise UserAlreadyExists(f"User {user_id} already exists in {self.tokens_file}")

        self._users[user_id] = User(user_info=user_info)
        log.debug("User %s added to %s", user_id, self.tokens_file)
        if self._default_user is None:
            self._default_user = user_id
            log.debug("User %s set as the default user ID", user_id)
        self._save()

    def get_users(self) -> dict[str, User]:
        """Return a dictionary of the users managed"""
        return deepcopy(self._users)

    def remove_user(self, user_id: str) -> None:
        """Remove a user to the list of managed users"""
        if user_id not in self._users:
            log.debug("User %s not removed from %s -- user did not exist",
                      user_id, self.tokens_file
                      )
            return

        del self._users[user_id]
        log.debug("Removed user %s from %s", user_id, self.tokens_file)

        # Update the default user if it was deleted
        if self._default_user == user_id:
            if self._users:
                self._default_user = list(self._users.keys())[0]
                log.debug("Changed default user to first available user %s", self._default_user)
            else:
                self._default_user = None

        self._save()

    def set_default_token(self, token: str) -> None:
        """Set the default user to the User ID with the specified token"""
        user_id = self._get_token_owner(token=token)
        if user_id is None:
            log.error("No user found with token %s ", token)
            raise NoSuchUser(f"No user found with token {token}")

        if self._default_user == user_id:
            return

        self._default_user = user_id
        self._save()
        log.debug("Set default user to %s for token %s", user_id, token)

    def set_default_user(self, user_id: str) -> None:
        """Set the default user to the specified User ID"""
        if user_id not in self._users:
            log.error("No user found with id %s ", user_id)
            raise NoSuchUser(f"No user found with id {user_id}")

        if self._default_user == user_id:
            return

        self._default_user = user_id
        self._save()
        log.debug("Default user set to %s", user_id)

    def update_token(self, user_id: str, token: str) -> None:
        """Update the token for the specified User ID"""
        if user_id not in self._users:
            log.error("No user found with id %s ", user_id)
            raise NoSuchUser(f"No user found with id {user_id}")

        if self._users[user_id].token == token:
            return

        self._users[user_id].token = token
        self._users[user_id].last_updated = datetime.now()
        self._save()
        log.debug("User id %s updated to token %s", user_id, token)

    @property
    def default_token_file(self) -> Path:
        """Return the path of the default token file"""
        return AOC_RUNNER_AUTH_DIR / "token"

    @property
    def default_user(self) -> str:
        """Return the current default user"""
        return self._default_user

    @property
    def tokens_file(self) -> Path:
        """Return the path of the tokens file"""
        return AOC_RUNNER_AUTH_DIR / "tokens.json"
