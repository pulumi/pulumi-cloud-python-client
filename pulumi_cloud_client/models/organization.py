"""Organization model for the Pulumi Cloud API client.

Defines the structure and properties of a Pulumi organization.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Organization:
    """Represents a Pulumi organization."""

    name: str
    display_name: Optional[str] = None
    github_login: Optional[str] = None
    created_on: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        """Return the organization name (for API consistency)."""
        return self.name

    @classmethod
    def from_api_response(cls, item: Dict[str, Any]) -> "Organization":
        """
        Create an Organization instance from an API response dictionary.

        Args:
            item: API response dictionary containing organization data

        Returns:
            An Organization instance
        """
        return cls(
            name=item["name"],
            display_name=item.get("displayName"),
            github_login=item.get("githubLogin"),
            created_on=(datetime.fromisoformat(item["createdOn"]) if item.get("createdOn") else None),
        )
