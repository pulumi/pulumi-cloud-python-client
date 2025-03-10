from typing import Any


class PulumiAPIError(Exception):
    """Exception raised for Pulumi API errors."""

    def __init__(self, status_code: int, message: str, response_data: Any = None):
        self.status_code = status_code
        self.message = message
        self.response_data = response_data
        super().__init__(f"Pulumi API Error ({status_code}): {message}")
