"""Stack model for the Pulumi Cloud API client.

Defines the structure and properties of a Pulumi stack.
"""

# pulumi_client/models/stack.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class StackResource:
    """Represents a single resource in a Pulumi stack."""

    resource_id: str
    type: str
    name: str
    provider: str
    parent: Optional[str]
    properties: Dict[str, Any]


@dataclass
class Stack:
    """Represents a Pulumi stack."""

    name: str
    organization: str
    project: str
    last_update: Optional[datetime]
    resource_count: int
    resources: Optional[List[StackResource]] = None
    description: Optional[str] = None
    tags: Optional[Dict[str, str]] = None

    @property
    def full_name(self) -> str:
        """Return the fully qualified stack name."""
        return f"{self.organization}/{self.project}/{self.name}"

    @classmethod
    def from_api_response(cls, item: Dict[str, Any]) -> "Stack":
        """
        Create a Stack instance from an API response dictionary.

        Args:
            item: API response dictionary containing stack data

        Returns:
            A Stack instance
        """
        return cls(
            name=item["name"],
            organization=item["orgName"],
            project=item["projectName"],
            last_update=(datetime.fromisoformat(item["lastUpdate"]) if item.get("lastUpdate") else None),
            resource_count=item.get("resourceCount", 0),
            description=item.get("description"),
            tags=item.get("tags", {}),
        )
