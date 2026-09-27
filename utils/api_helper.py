"""
API Helper
==========
Lightweight requests-based utility for API test setup/teardown
and pre-condition verification.

Usage:
    from utils.api_helper import APIHelper

    api = APIHelper(base_url="https://api.example.com")
    response = api.get("/users/1")
    api.post("/setup", json={"key": "value"})
"""

from __future__ import annotations

from typing import Any

import requests

from utils.exceptions import APIRequestError
from utils.logger import get_logger

logger = get_logger(__name__)


class APIHelper:
    """Simple HTTP client for test setup and teardown."""

    def __init__(
        self,
        base_url: str = "",
        headers: dict[str, str] | None = None,
        timeout: int = 30,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout

        if headers:
            self.session.headers.update(headers)

    # ── HTTP Methods ──────────────────────────────────────────
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Send a GET request."""
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Send a POST request."""
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Send a PUT request."""
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Send a DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """Send a PATCH request."""
        return self._request("PATCH", endpoint, **kwargs)

    # ── Core Request ──────────────────────────────────────────
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Execute an HTTP request with logging and error handling."""
        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        kwargs.setdefault("timeout", self.timeout)

        logger.info("API %s %s", method, url)

        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(
                "API %s %s → %d (%dms)",
                method,
                url,
                response.status_code,
                int(response.elapsed.total_seconds() * 1000),
            )
            return response
        except requests.RequestException as e:
            raise APIRequestError(method, url, reason=str(e))

    # ── Convenience ───────────────────────────────────────────
    def get_json(self, endpoint: str, **kwargs) -> Any:
        """GET and return parsed JSON."""
        resp = self.get(endpoint, **kwargs)
        return resp.json()

    def post_json(self, endpoint: str, data: dict, **kwargs) -> Any:
        """POST JSON and return parsed response."""
        resp = self.post(endpoint, json=data, **kwargs)
        return resp.json()

    def assert_status(
        self, response: requests.Response, expected: int = 200
    ) -> requests.Response:
        """Assert response status code."""
        if response.status_code != expected:
            raise APIRequestError(
                response.request.method,
                response.url,
                status_code=response.status_code,
                reason=f"Expected {expected}, got {response.status_code}",
            )
        return response
