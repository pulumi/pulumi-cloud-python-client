"""Policy model for the Pulumi Cloud API client.

Defines the structure and properties of Pulumi policies.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PolicyPack:
    """Represents a Pulumi Policy Pack."""

    name: str
    display_name: Optional[str] = None
    version: Optional[str] = None
    publisher: Optional[str] = None
    description: Optional[str] = None
    organization: Optional[str] = None
    is_organizational: Optional[bool] = None
    created_at: Optional[str] = None

    @property
    def full_name(self) -> str:
        """Get the full name of the policy pack."""
        if self.organization:
            return f"{self.organization}/{self.name}"
        return self.name

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "PolicyPack":
        """
        Create a PolicyPack instance from API response data.

        Args:
            data: The API response data

        Returns:
            A PolicyPack instance
        """
        return cls(
            name=data["name"],
            display_name=data.get("displayName"),
            version=data.get("version"),
            publisher=data.get("publisher"),
            description=data.get("description"),
            organization=data.get("organization"),
            is_organizational=data.get("isOrganizational"),
            created_at=data.get("createdAt"),
        )
