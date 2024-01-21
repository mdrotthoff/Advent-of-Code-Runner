"""Provide a common HTTP client used to communicate
with the Advent of Code servers.
"""

# System libraries
from collections import deque
import logging
from os import environ
import time
import urllib3

# Advent of Code Runner libraries
from .config import __version__


log = logging.getLogger(__name__)
USER_AGENT = f"advent-of-code-runner v{__version__} by drotthoff@gmail.com"


class HttpClient:
    """Every request to the Advent of Code servers goes through this class.
    It provides support to add a requested user agent header and enforce rate
    limiting.
    """

    def __init__(self):
        """Initialize the HTTP Client class"""
        proxy_url = environ.get("http_proxy") or environ.get("https_proxy")

        if proxy_url:
            self._pool_manager = urllib3.ProxyManager(
                proxy_url, headers={"User-Agent": USER_AGENT}
            )
        else:
            self._pool_manager = urllib3.PoolManager(headers={"User-Agent": USER_AGENT})

        self.req_count = {"GET": 0, "POST": 0}
        self._max_t = 3.0
        self._cool_off = 0.25
        self._history = deque([time.time() - self._max_t] * 4, maxlen=4)

    def _limiter(self):
        """Ensure that the Advent of Code servers are not accessed too fast."""
        now = time.time()
        t0 = self._history[0]

        if now - t0 < self._max_t:
            msg = "You are being rate-limited - slow down on the requests! (delay=%.02fs)"
            log.warning(msg, self._cool_off)
            time.sleep(self._cool_off)
            self._cool_off *= 2  # double it for repeat offenders

        self._history.append(now)

    def get(self, url, token=None, redirect=True):
        """Issue an HTTP GET request to the Advent of Code servers"""
        print(f"Running http_client.get for token {token}")
        if token is None:
            headers = self._pool_manager.headers
        else:
            headers = self._pool_manager.headers | {"Cookie": f"session={token}"}

        self._limiter()
        resp = self._pool_manager.request(
            method="GET", url=url, headers=headers, redirect=redirect
        )
        self.req_count["GET"] += 1
        return resp

    def post(self, url, token, fields):
        """Issue an HTTP POST request to the Advent of Code servers"""
        print(f"Running http_client.post for token {token}")
        headers = self._pool_manager.headers | {"Cookie": f"session={token}"}
        self._limiter()
        resp = self._pool_manager.request_encode_body(
            method="POST",
            url=url,
            fields=fields,
            headers=headers,
            encode_multipart=False,
        )
        self.req_count["POST"] += 1
        return resp


# Create an instance of the HttpClient for common use
http_client = HttpClient()
