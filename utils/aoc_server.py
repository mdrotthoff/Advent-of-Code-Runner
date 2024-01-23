"""Access the Advent of Code servers"""

# System libraries
from pathlib import Path
import pickle

# Advent of Code Runner libraries
from aoc_runner.httpclient import http_client
from aoc_runner.config import AOC_DOMAIN, AOC_RUNNER_PROJECT_HOME


print(f"CWD: {Path().cwd()}")
if AOC_RUNNER_PROJECT_HOME:
    data_path = AOC_RUNNER_PROJECT_HOME
else:
    data_path = Path().cwd()
data_path = data_path / "data" / "home"
print(f"Data path: {data_path}")

if not data_path.exists():
    data_path.mkdir(parents=True, exist_ok=True)
elif data_path.is_file():
    raise ValueError(f"Data path is file not directory: {str(data_path)}")

url = f"{AOC_DOMAIN}"
source = 'home'

html_file_name = data_path / f"{source}.html"
pickle_file_name = data_path / f"{source}.pickle"

if pickle_file_name.exists():
    print(f"Cached Advent of Code home page already exists")
else:
    response = http_client.get(url=url, token=None, redirect=False)
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
        print("Advent of Code home page cached")
