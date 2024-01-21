"""Defined the exceptions used by Advent of Code Runner"""


class AocRunnerException(Exception):
    """Defined the base exception for the Advent of Code Runner library"""


class AocValueError(AocRunnerException):
    """The value is not valid"""


class DeadTokenError(AocRunnerException):
    """The token is no longer valid"""


class DirectoryIsFile(AocRunnerException):
    """A file was found were a directory was expected"""


class MissingSessionToken(AocRunnerException):
    """No valid session token was found"""


class NoSuchUser(AocRunnerException):
    """No valid session token was found"""


class TokenFileChanged(AocRunnerException):
    """No valid session token was found"""


class UnknownLoginSource(AocRunnerException):
    """Log in source not recognized"""


class UserAlreadyExists(AocRunnerException):
    """User ID is already in tokens.json"""
