"""Client library for interacting with the Pulumi Cloud API.

This module provides the main client interface for accessing Pulumi Cloud resources.
"""

import json
import time
from typing import Any, Dict, Optional

import requests

from pulumi_cloud_client.exceptions import PulumiAPIError

from .resources.organizations import OrganizationsResource
from .resources.policies import PoliciesResource
from .resources.projects import ProjectsResource
from .resources.stacks import StacksResource


class PulumiClient:
    """Client for the Pulumi Service Admin API."""

    def __init__(
        self,
        access_token: str,
        base_url: str = "https://api.pulumi.com",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1,
    ):
        """
        Initialize the Pulumi API client.

        Args:
            access_token: The API access token for authentication
            base_url: Base URL for the Pulumi API (defaults to https://api.pulumi.com)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts for recoverable errors
            retry_delay: Initial delay between retries in seconds (increases exponentially)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        self.stacks = StacksResource(self)
        self.projects = ProjectsResource(self)
        self.organizations = OrganizationsResource(self)
        self.policies = PoliciesResource(self)

    def _handle_response(self, response: requests.Response) -> Any:
        """Process API response and handle errors."""
        try:
            response.raise_for_status()
            if response.content:
                return response.json()
            return None
        except requests.HTTPError:
            error_data = None
            error_message = response.reason

            try:
                error_data = response.json()
                if isinstance(error_data, dict) and "message" in error_data:
                    error_message = error_data["message"]
            except (json.JSONDecodeError, ValueError):
                # Only catch JSON parsing errors, not all exceptions
                pass

            raise PulumiAPIError(
                status_code=response.status_code,
                message=error_message,
                response_data=error_data,
            )

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Send a request to the Pulumi API with retry logic.

        Args:
            method: HTTP method (get, post, put, patch, delete)
            path: API endpoint path
            params: URL parameters to include
            data: JSON body data

        Returns:
            Parsed API response
        """
        url = f"{self.base_url}/{path.lstrip('/')}"

        retries = 0
        delay = self.retry_delay

        while True:
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=self.timeout,
                )
                return self._handle_response(response)
            except (requests.RequestException, PulumiAPIError) as e:
                retries += 1

                # Determine if error is retryable
                retryable = False
                if isinstance(e, requests.RequestException):
                    # Network errors are retryable
                    retryable = True
                elif isinstance(e, PulumiAPIError) and e.status_code in (
                    429,
                    500,
                    502,
                    503,
                    504,
                ):
                    # Rate limits and server errors are retryable
                    retryable = True

                if not retryable or retries > self.max_retries:
                    raise

                # Exponential backoff with jitter
                time.sleep(delay * (0.9 + 0.2 * (retries / self.max_retries)))
                delay *= 2

    # General purpose request method
    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make a custom API request for endpoints not explicitly covered.

        Args:
            method: HTTP method (get, post, put, patch, delete)
            path: API endpoint path
            params: URL parameters to include
            data: JSON body data

        Returns:
            Parsed API response
        """
        return self._make_request(method.lower(), path, params, data)
