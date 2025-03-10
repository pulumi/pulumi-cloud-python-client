#!/usr/bin/env python3
"""Example script demonstrating how to transfer all stacks between organizations."""

import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Tuple

from pulumi_cloud_client.client import PulumiClient
from pulumi_cloud_client.exceptions import PulumiAPIError
from pulumi_cloud_client.models.stack import Stack


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Transfer all stacks from source organization to destination organization"
    )
    parser.add_argument("--source-org", "-s", required=True, help="Source organization name")
    parser.add_argument("--dest-org", "-d", required=True, help="Destination organization name")
    parser.add_argument("--project", "-p", help="Optional: Only transfer stacks for a specific project")
    parser.add_argument("--parallel", type=int, default=4, help="Number of parallel transfers (default: 4)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run, don't actually transfer stacks")
    return parser.parse_args()


def transfer_stack(client: PulumiClient, stack: Stack, dest_org: str, dry_run: bool = False) -> Tuple[Stack, str, bool]:
    """
    Transfer a single stack to the destination organization.

    Handles all necessary steps to move a stack between organizations including
    permissions and configuration.

    Args:
        client: PulumiClient instance
        stack: Stack to transfer
        dest_org: Destination organization name
        dry_run: If True, only simulate the transfer

    Returns:
        Tuple of (stack, message, success_flag)
    """
    try:
        if dry_run:
            return stack, f"Would transfer stack {stack.full_name} to {dest_org} (dry run)", True

        transferred_stack = client.stacks.transfer_stack(
            org_name=stack.organization, project_name=stack.project, stack_name=stack.name, new_org_name=dest_org
        )
        return transferred_stack, f"Successfully transferred {stack.full_name} to {dest_org}", True
    except PulumiAPIError as e:
        return stack, f"Error transferring {stack.full_name}: {e.message} (Status: {e.status_code})", False


def main():
    """Transfer all stacks between organizations."""
    args = get_args()

    # Configure authentication
    access_token = os.environ.get("PULUMI_ACCESS_TOKEN")
    if not access_token:
        print("Error: PULUMI_ACCESS_TOKEN environment variable not set")
        sys.exit(1)

    # Initialize Pulumi API client
    client = PulumiClient(access_token=access_token)

    try:
        # Get all stacks in source organization, optionally filtered by project
        if args.project:
            stacks = client.stacks.list(args.source_org, args.project)
            print(f"Found {len(stacks)} stacks in organization '{args.source_org}' project '{args.project}'")
        else:
            stacks = client.stacks.list(args.source_org)
            print(f"Found {len(stacks)} stacks in organization '{args.source_org}'")

        if not stacks:
            print("No stacks found to transfer.")
            return

        # Print stack list
        print("\nStacks to transfer:")
        for i, stack in enumerate(stacks, 1):
            print(f"{i}. {stack.full_name} (Last updated: {stack.last_update}, Resources: {stack.resource_count})")

        # Confirm if not dry run
        if not args.dry_run:
            confirm = input(f"\nTransfer {len(stacks)} stacks from '{args.source_org}' to '{args.dest_org}'? (y/n): ")
            if confirm.lower() != "y":
                print("Transfer cancelled.")
                return
        else:
            print("\nRunning in dry-run mode, no actual transfers will be performed.")

        # Track results
        results: Dict[str, int] = {"successful": 0, "failed": 0}

        # Transfer stacks in parallel
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            future_to_stack = {
                executor.submit(transfer_stack, client, stack, args.dest_org, args.dry_run): stack for stack in stacks
            }

            print("\nTransferring stacks...")
            for i, future in enumerate(as_completed(future_to_stack), 1):
                stack, message, success = future.result()
                print(f"[{i}/{len(stacks)}] {message}")

                if success:
                    results["successful"] += 1
                else:
                    results["failed"] += 1

        # Print summary
        print("\nTransfer summary:")
        print(f"  Total stacks: {len(stacks)}")
        print(f"  Successfully transferred: {results['successful']}")
        print(f"  Failed transfers: {results['failed']}")

    except PulumiAPIError as e:
        print(f"API Error: {e.message} (Status code: {e.status_code})")
        if e.response_data:
            print(f"Response details: {e.response_data}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting transfer process")
    main()
