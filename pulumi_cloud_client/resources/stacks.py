"""Stacks resource for the Pulumi Cloud API client.

Provides methods for interacting with Pulumi stacks.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models import Stack


class StacksResource:
    """Handles API interactions for Pulumi stacks."""

    def __init__(self, client):
        """Initialize the Stacks resource.

        Args:
            client: The Pulumi client instance to use for API calls.
        """
        self.client = client

    def list(self, org_name: str, project_name: Optional[str] = None) -> List[Stack]:
        """List stacks for an organization or project."""
        path = f"/api/stacks/{org_name}"
        if project_name:
            path += f"/{project_name}"

        response = self.client._make_request("get", path)

        # Use the from_api_response method to create instances
        return [Stack.from_api_response(item) for item in response]

    def get(self, org_name: str, project_name: str, stack_name: str) -> Stack:
        """
        Get stack details.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name

        Returns:
            Stack object
        """
        response = self.client._make_request("get", f"/api/stacks/{org_name}/{project_name}/{stack_name}")
        return Stack.from_api_response(response)

    def get_latest_update(self, org_name: str, project_name: str, stack_name: str) -> Dict[str, Any]:
        """
        Get the latest update for a stack.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name

        Returns:
            Latest update details
        """
        return self.client._make_request("get", f"/api/stacks/{org_name}/{project_name}/{stack_name}/updates/latest")

    def get_update(self, org_name: str, project_name: str, stack_name: str, update_id: str) -> Dict[str, Any]:
        """
        Get a specific update for a stack.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name
            update_id: Update ID

        Returns:
            Update details
        """
        return self.client._make_request(
            "get",
            f"/api/stacks/{org_name}/{project_name}/{stack_name}/updates/{update_id}",
        )

    def list_tags(self, org_name: str, project_name: str, stack_name: str) -> Dict[str, str]:
        """
        List tags for a stack.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name

        Returns:
            Dictionary of tag key-value pairs
        """
        return self.client._make_request("get", f"/api/stacks/{org_name}/{project_name}/{stack_name}/tags")

    def update_tags(self, org_name: str, project_name: str, stack_name: str, tags: Dict[str, str]) -> None:
        """
        Update tags for a stack.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name
            tags: Dictionary of tag key-value pairs
        """
        self.client._make_request(
            "patch",
            f"/api/stacks/{org_name}/{project_name}/{stack_name}/tags",
            data=tags,
        )

    def export_deployment(self, org_name: str, project_name: str, stack_name: str) -> Dict[str, Any]:
        """
        Export the latest deployment for a stack.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name

        Returns:
            Deployment data
        """
        return self.client._make_request("get", f"/api/stacks/{org_name}/{project_name}/{stack_name}/export")

    def create_stack(self, org_name: str, project_name: str, stack_name: str) -> Stack:
        """
        Create a new stack.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name

        Returns:
            Stack object
        """
        data = {"orgName": org_name, "projectName": project_name, "stackName": stack_name}
        response = self.client._make_request("post", f"/api/stacks/{org_name}/{project_name}/{stack_name}", data=data)
        return Stack(
            name=response["name"],
            organization=response["orgName"],
            project=response["projectName"],
            last_update=(datetime.fromisoformat(response["lastUpdate"]) if response.get("lastUpdate") else None),
            resource_count=response.get("resourceCount", 0),
        )

    def delete_stack(self, org_name: str, project_name: str, stack_name: str) -> None:
        """
        Delete a stack.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name
        """
        self.client._make_request("delete", f"/api/stacks/{org_name}/{project_name}/{stack_name}")

    def update_stack(self, org_name: str, project_name: str, stack_name: str, data: Dict[str, Any]) -> Stack:
        """
        Update a stack.

        Args:
            org_name: Organization name
            project_name: Project name
            stack_name: Stack name
            data: Dictionary of stack properties to update

        Returns:
            Stack object
        """
        response = self.client._make_request("patch", f"/api/stacks/{org_name}/{project_name}/{stack_name}", data=data)
        return Stack(
            name=response["name"],
            organization=response["orgName"],
            project=response["projectName"],
            last_update=(datetime.fromisoformat(response["lastUpdate"]) if response.get("lastUpdate") else None),
            resource_count=response.get("resourceCount", 0),
        )

    def transfer_stack(self, org_name: str, project_name: str, stack_name: str, new_org_name: str) -> Stack:
        """
        Transfer a stack to a new organization.

        Args:
            org_name: Current organization name
            project_name: Project name
            stack_name: Stack name
            new_org_name: New organization name

        Returns:
            Stack object
        """
        data = {"toOrg": new_org_name}
        response = self.client._make_request(
            "post", f"/api/stacks/{org_name}/{project_name}/{stack_name}/transfer", data=data
        )
        return Stack.from_api_response(response)


class Stacks:
    """Handles API interactions for Pulumi stacks.

    This class provides a wrapper for stack operations in the Pulumi Cloud,
    allowing users to create, list, update, and manage stacks.
    """

    def __init__(self, client):
        """Initialize the Stacks resource.

        Args:
            client: The Pulumi client instance to use for API calls.
        """
        self.client = client
