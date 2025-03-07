"""Organizations resource for the Pulumi Cloud API client.

Provides methods for interacting with Pulumi organizations.
"""

from typing import Any, Dict, List

from ..models.organization import Organization


class OrganizationsResource:
    """Handles API interactions for Pulumi organizations.

    This class provides methods to list, get, and manage organizations
    and their team members in the Pulumi Cloud.
    """

    def __init__(self, client):
        """Initialize the Organizations resource.

        Args:
            client: The Pulumi client instance to use for API calls.
        """
        self.client = client

    def list(self) -> List[Organization]:
        """
        List organizations the caller has access to.

        Returns:
            List of organization objects
        """
        response = self.client._make_request("get", "/api/user/organizations")
        return [Organization.from_api_response(item) for item in response]

    def get(self, org_name: str) -> Organization:
        """
        Get organization details.

        Args:
            org_name: Organization name

        Returns:
            Organization details
        """
        response = self.client._make_request("get", f"/api/organizations/{org_name}")
        return Organization.from_api_response(response)

    def list_team_members(self, org_name: str) -> List[Dict[str, Any]]:
        """
        List team members for an organization.

        Args:
            org_name: Organization name

        Returns:
            List of team member objects
        """
        return self.client._make_request("get", f"/api/organizations/{org_name}/members")

    def invite_user(self, org_name: str, email: str, role: str = "member") -> Dict[str, Any]:
        """
        Invite a user to an organization.

        Args:
            org_name: Organization name
            email: User email
            role: User role ('admin' or 'member')

        Returns:
            Invitation details
        """
        return self.client._make_request(
            "post",
            f"/api/organizations/{org_name}/members",
            data={"email": email, "role": role},
        )
