"""Policies resource for the Pulumi Cloud API client.

Provides methods for interacting with Pulumi policies.
"""

from typing import List

from pulumi_cloud_client.models.policy import PolicyPack


class PoliciesResource:
    """Resource for managing Pulumi Policy Packs."""

    def __init__(self, client):
        """
        Initialize the Policies resource.

        Args:
            client: The Pulumi API client instance
        """
        self.client = client

    def list(self, org_name: str) -> List[PolicyPack]:
        """
        List policy packs for an organization.

        Args:
            org_name: Organization name

        Returns:
            List of policy pack objects
        """
        response = self.client._make_request("get", f"/api/organizations/{org_name}/policy-packs")
        return [PolicyPack.from_api_response(item) for item in response]

    def get(self, org_name: str, policy_pack_name: str, version: str) -> PolicyPack:
        """
        Get policy pack details.

        Args:
            org_name: Organization name
            policy_pack_name: Policy pack name
            version: Policy pack version

        Returns:
            Policy pack details
        """
        response = self.client._make_request(
            "get",
            f"/api/organizations/{org_name}/policy-packs/{policy_pack_name}/versions/{version}",
        )
        return PolicyPack.from_api_response(response)
