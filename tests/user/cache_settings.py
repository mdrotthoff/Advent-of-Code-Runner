"""Get the settings page for a specificied token from the Advent of Code servers"""

# System libraries
from pathlib import Path
import pickle

# Advent of Code Runner libraries
from aoc_runner.config import AOC_DOMAIN
from aoc_runner.httpclient import http_client

URL = f"{AOC_DOMAIN}/settings"
TOKENS_TO_CACHE = {
    "github": "53616c7465645f5f9ae2b7d2af32fc2e3862adb2f08e5a4dc66b594dd1ad760543ad850fd3692a496e07e3993106607dce2a5bfa13aa311d419223b4fd12e564",
    "google": "53616c7465645f5f6a517bc02d328a3ecfc5bf02ef49ea4e8a981cfd9bb9f6e51ddbaa6601ce7b79c8ee3405d77dad4016f17640ef249adbb78045b2c6e645e7",
    "expired": "53616c7465645f5f168e2a3588960815d03e3b36461ae4d80d2d4918cbdcba3b9a08a1becf6134815911e83eb748e180ff28aa7abd71e5e28ec15a601603e03b",
}


def cache_settings(token: str, source: str) -> None:
    """Cache the user settings page for the specified token"""

    file_name = Path("data") / f"settings_{token}.pickle"
    if file_name.exists():
        print(f"Cached user settings response for {source} already exists")
        return

    response = http_client.get(URL, token=token, redirect=False)
    response._pool = None
    with open(file_name, mode="wb") as file:
        pickle.dump(response, file)

    with open(file_name, mode="rb") as file:
        loaded = pickle.load(file)

    if (
            loaded.data == response.data
            and loaded.headers == response.headers
            and loaded.status == response.status
    ):
        print(f"User settings for {source} cached")


def main():
    """Cache each the tokens in the provided token dictionary"""
    for source, token in TOKENS_TO_CACHE.items():
        cache_settings(token=token, source=source)


# If run as a script, execute the main function
if __name__ == "__main__":
    main()
