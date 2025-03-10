# Examples

This directory contains example scripts demonstrating how to use the Pulumi Cloud Python Client.

## Basic Usage

```python
from pulumi_cloud_client.client import PulumiClient

# Initialize client
client = PulumiClient(
    access_token="your-access-token-here",
    base_url="https://api.pulumi.com"
)
```

## Transfer All Stacks

Transfers all stacks from one organization to another.

```bash
# Set your Pulumi access token
export PULUMI_ACCESS_TOKEN=your_access_token

# Transfer all stacks from source-org to destination-org
python transfer_all_stacks.py -s source-org -d destination-org

# Transfer only stacks from a specific project
python transfer_all_stacks.py -s source-org -d destination-org -p my-project

# Do a dry run first to see what would be transferred
python transfer_all_stacks.py -s source-org -d destination-org --dry-run
```

## Transfer Single Stack

Transfers a specific stack from one organization to another.

```bash
# Set your Pulumi access token
export PULUMI_ACCESS_TOKEN=your_access_token

# Edit the script to set your source and destination organizations
# and run it
python transfer_stack_between_orgs.py
```

## List Stacks

Shows how to list organizations, projects, and stacks.

```bash
# Set your access token in the script or use an environment variable
# Edit the example as needed and run it
python stacks.py
```

## Common Tasks

Each example demonstrates common tasks you might want to perform with the Pulumi API:

1. Authentication with the Pulumi API
2. Listing and filtering resources
3. Working with organizations and projects
4. Managing stack operations
5. Error handling

For more details on the available API methods, refer to the client documentation.
