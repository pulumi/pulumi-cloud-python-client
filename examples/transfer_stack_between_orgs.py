"""Example script demonstrating how to transfer a stack between organizations."""

import os

from pulumi_cloud_client.client import PulumiClient
from pulumi_cloud_client.exceptions import PulumiAPIError


def transfer_stack_between_orgs(args):
    """Transfer a Pulumi stack from one organization to another.

    Args:
        args: Command line arguments containing source and destination information.
    """
    # Configure authentication via environment variable
    # export PULUMI_ACCESS_TOKEN=your_access_token
    access_token = os.environ.get("PULUMI_ACCESS_TOKEN")
    if not access_token:
        print("Error: PULUMI_ACCESS_TOKEN environment variable not set")
        return

    # Initialize Pulumi API client
    client = PulumiClient(access_token=access_token, base_url="https://api.pulumi.com", timeout=30)

    # Define source organization and stack
    source_org = "source-organization"
    project = "my-project"
    stack_name = "dev"

    # Define destination organization
    destination_org = "destination-organization"

    try:
        # Execute the transfer stack operation using the client library
        stack = client.stacks.transfer_stack(
            org_name=source_org, project_name=project, stack_name=stack_name, new_org_name=destination_org
        )

        print("Stack transfer initiated successfully!")
        print(f"Stack {project}/{stack_name} transferred from {source_org} to {destination_org}")
        print(f"New stack full name: {stack.full_name}")
        print("Transfer completed successfully")

    except PulumiAPIError as e:
        print(f"Error transferring stack: {e.message} (Status code: {e.status_code})")
        if e.response_data:
            print(f"Response details: {e.response_data}")


if __name__ == "__main__":
    transfer_stack_between_orgs(None)  # Replace None with actual args when needed
