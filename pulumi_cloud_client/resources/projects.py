"""Projects resource for the Pulumi Cloud API client.

Provides methods for interacting with Pulumi projects.
"""

from typing import List

from ..models.project import Project


class ProjectsResource:
    """Handles API interactions for Pulumi projects."""

    def __init__(self, client):
        """Initialize the Projects resource.

        Args:
            client: The Pulumi client instance to use for API calls.
        """
        self.client = client

    def list(self, org_name: str) -> List[Project]:
        """
        List projects for an organization.

        Args:
            org_name: Organization name

        Returns:
            List of project objects
        """
        response = self.client._make_request("get", f"/api/organizations/{org_name}/projects")

        # Use the from_api_response method to create instances
        return [Project.from_api_response(item, org_name) for item in response]

    def get(self, org_name: str, project_name: str) -> Project:
        """
        Get project details.

        Args:
            org_name: Organization name
            project_name: Project name

        Returns:
            Project details
        """
        response = self.client._make_request("get", f"/api/organizations/{org_name}/projects/{project_name}")
        return Project.from_api_response(response, org_name)
