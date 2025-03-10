"""Project model for the Pulumi Cloud API client.

Defines the structure and properties of a Pulumi project.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Project:
    """Represents a Pulumi project."""

    name: str
    organization: str
    description: Optional[str] = None
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    runtime: Optional[str] = None

    @property
    def full_name(self) -> str:
        """Return the fully qualified project name."""
        return f"{self.organization}/{self.name}"

    @classmethod
    def from_api_response(cls, item: Dict[str, Any], org_name: str) -> "Project":
        """
        Create a Project instance from an API response dictionary.

        Args:
            item: API response dictionary containing project data
            org_name: The organization name (may not be in the response)

        Returns:
            A Project instance
        """
        return cls(
            name=item["name"],
            organization=org_name,
            description=item.get("description"),
            runtime=item.get("runtime"),
            created_on=(datetime.fromisoformat(item["createdOn"]) if item.get("createdOn") else None),
            updated_on=(datetime.fromisoformat(item["lastUpdated"]) if item.get("lastUpdated") else None),
        )
