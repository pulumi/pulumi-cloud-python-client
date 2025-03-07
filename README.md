# Pulumi Cloud Python Client

A Python client library for interacting with the Pulumi Cloud API. This client provides a simple interface for managing Pulumi resources programmatically, including stacks, projects, organizations, and policies.

## Installation

Install the package using pip:

```bash
pip install pulumi-cloud-client
```

Or with Poetry:

```bash
poetry add pulumi-cloud-client
```

## Authentication

Authentication is handled using a Pulumi access token:

```python
from pulumi_cloud_client.client import PulumiClient

# Authenticate with token from environment variable
client = PulumiClient(
    access_token="your-pulumi-access-token",
    base_url="https://api.pulumi.com"  # Optional, defaults to https://api.pulumi.com
)
```

## Usage Examples

### List Organizations

```python
# List all organizations you have access to
organizations = client.organizations.list()
for org in organizations:
    print(f"Organization: {org.name}")
```

### Working with Projects

```python
# List projects in an organization
projects = client.projects.list("my-organization")
for project in projects:
    print(f"Project: {project.name}")

# Get a specific project
project = client.projects.get("my-organization", "my-project")
```

### Managing Stacks

```python
# List stacks in a project
stacks = client.stacks.list("my-organization", "my-project")
for stack in stacks:
    print(f"Stack: {stack.full_name}, Resources: {stack.resource_count}")

# Get stack details
stack = client.stacks.get("my-organization", "my-project", "dev")

# Update stack tags
client.stacks.update_tags("my-organization", "my-project", "dev", {"environment": "development"})
```

### Transferring Stacks

```python
# Transfer a stack to a different organization
transferred_stack = client.stacks.transfer_stack(
    "source-org", "my-project", "dev", "destination-org"
)
print(f"Stack transferred to: {transferred_stack.full_name}")
```

## API Reference

### Core Resources

- **Stacks**: Create, list, update, delete, and transfer stacks
- **Projects**: List and get project details
- **Organizations**: List organizations and manage team members
- **Policies**: List and get policy packs

### Error Handling

The client raises `PulumiAPIError` for API-related errors:

```python
from pulumi_cloud_client.exceptions import PulumiAPIError

try:
    client.stacks.get("org", "project", "non-existent-stack")
except PulumiAPIError as e:
    print(f"API Error: {e.message} (Status code: {e.status_code})")
```

## Examples

See the [examples directory](examples/README.md) for more detailed examples of how to use the client.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
