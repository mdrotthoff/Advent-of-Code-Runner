"""Access the Advent of Code server settings page to capture real responses"""

# System libraries
from os import getenv
from pathlib import Path
import pickle

# Advent of Code Runner libraries
from aoc_runner.config import AOC_DOMAIN, AOC_RUNNER_PROJECT_HOME
from aoc_runner.httpclient import http_client


url = f"{AOC_DOMAIN}/settings"
tokens = {
    "github": "53616c7465645f5fdbbad2d94679841bdf9942dc43b005a783a0eea2a49c5561bafd171b9306dca8b344ebec1215d33d7364ad1b9e015431a59053ef92353ec6",
    "google": "53616c7465645f5f9acdce89d892a711d5b8967226d0f1da8bb5c373b85929b8efbba7a248b11a7c90cb914d2b31f697cdc80cad7012b17781e6fd21bb479731",
    "expire": "53616c7465645f5f168e2a3588960815d03e3b36461ae4d80d2d4918cbdcba3b9a08a1becf6134815911e83eb748e180ff28aa7abd71e5e28ec15a601603e03b",
}

print(f"CWD: {Path().cwd()}")
if AOC_RUNNER_PROJECT_HOME:
    data_path = AOC_RUNNER_PROJECT_HOME
else:
    data_path = Path().cwd()
data_path = data_path / "data" / "settings"
print(f"Data path: {data_path}")

if not data_path.exists():
    data_path.mkdir(parents=True, exist_ok=True)
elif data_path.is_file():
    raise ValueError(f"Data path is file not directory: {str(data_path)}")


for source, token in tokens.items():
    html_file_name = data_path / f"{source}.html"
    pickle_file_name = data_path / f"{source}.pickle"
    if pickle_file_name.exists() and html_file_name.exists():
        print(f"Cached user settings response for {source} already exists")
        continue

    response = http_client.get(url=url, token=token, redirect=False)
    response._pool = None

    with open(html_file_name, mode="w", encoding="utf-8") as file:
        if response.status == 200:
            file.write(response.data.decode(encoding="utf-8"))
        else:
            file.write(f"Status: {response.status}\nLocation: {response.get_redirect_location()}")

    # Pickle the response for a latter reload
    with open(pickle_file_name, mode="wb") as file:
        pickle.dump(response, file)

    with open(pickle_file_name, mode="rb") as file:
        loaded = pickle.load(file)

    if (
            loaded.data == response.data
            and loaded.headers == response.headers
            and loaded.status == response.status
    ):
        print(f"User settings for {source} cached")
