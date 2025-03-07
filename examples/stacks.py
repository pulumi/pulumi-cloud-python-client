"""Example script demonstrating how to work with Pulumi stacks using the client."""

from pulumi_cloud_client.client import PulumiClient

# Example usage:
if __name__ == "__main__":
    # Initialize client
    client = PulumiClient(
        access_token="your-access-token-here",
        base_url="https://api.pulumi.com",
        max_retries=3,
    )

    # List organizations
    orgs = client.organizations.list()
    print(f"Found {len(orgs)} organizations")

    # If organizations exist, get the first one's name
    if orgs:
        org_name = orgs[0].name

        # List projects for the organization
        projects = client.projects.list(org_name)
        print(f"Found {len(projects)} projects in {org_name}")

        # If projects exist, get the first one's name
        if projects:
            project_name = projects[0].name

            # List stacks for the project
            stacks = client.stacks.list(org_name, project_name)
            print(f"Found {len(stacks)} stacks in {project_name}")
