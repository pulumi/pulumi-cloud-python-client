import unittest
from unittest.mock import Mock

from pulumi_cloud_client.models.stack import Stack
from pulumi_cloud_client.resources.stacks import StacksResource


class TestStacksResource(unittest.TestCase):
    """Tests for the StacksResource class."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.mock_client = Mock()
        self.stacks_resource = StacksResource(self.mock_client)

        # Common test data
        self.org_name = "test-org"
        self.project_name = "test-project"
        self.stack_name = "test-stack"

    def test_list(self):
        """Test listing stacks."""
        # Mock API response
        mock_response = [
            {
                "name": "dev",
                "orgName": self.org_name,
                "projectName": self.project_name,
                "lastUpdate": "2023-01-01T12:00:00Z",
                "resourceCount": 5,
            },
            {
                "name": "prod",
                "orgName": self.org_name,
                "projectName": self.project_name,
                "lastUpdate": "2023-01-02T14:00:00Z",
                "resourceCount": 10,
            },
        ]
        self.mock_client._make_request.return_value = mock_response

        # Call the method
        result = self.stacks_resource.list(self.org_name, self.project_name)

        # Assertions
        self.mock_client._make_request.assert_called_once_with(
            "get", f"/api/stacks/{self.org_name}/{self.project_name}"
        )
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Stack)
        self.assertEqual(result[0].name, "dev")
        self.assertEqual(result[0].organization, self.org_name)
        self.assertEqual(result[0].project, self.project_name)
        self.assertEqual(result[0].resource_count, 5)
        self.assertEqual(result[1].name, "prod")

    def test_list_org_only(self):
        """Test listing stacks for an organization without specifying a project."""
        # Mock API response
        mock_response = [
            {
                "name": "dev",
                "orgName": self.org_name,
                "projectName": "project1",
                "resourceCount": 3,
            },
            {
                "name": "prod",
                "orgName": self.org_name,
                "projectName": "project2",
                "resourceCount": 7,
            },
        ]
        self.mock_client._make_request.return_value = mock_response

        # Call the method
        result = self.stacks_resource.list(self.org_name)

        # Assertions
        self.mock_client._make_request.assert_called_once_with("get", f"/api/stacks/{self.org_name}")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].project, "project1")
        self.assertEqual(result[1].project, "project2")

    def test_get(self):
        """Test getting a single stack."""
        # Mock API response
        mock_response = {
            "name": self.stack_name,
            "orgName": self.org_name,
            "projectName": self.project_name,
            "lastUpdate": "2023-01-01T12:00:00Z",
            "resourceCount": 5,
        }
        self.mock_client._make_request.return_value = mock_response

        # Call the method
        result = self.stacks_resource.get(self.org_name, self.project_name, self.stack_name)

        # Assertions
        self.mock_client._make_request.assert_called_once_with(
            "get", f"/api/stacks/{self.org_name}/{self.project_name}/{self.stack_name}"
        )
        self.assertIsInstance(result, Stack)
        self.assertEqual(result.name, self.stack_name)
        self.assertEqual(result.organization, self.org_name)
        self.assertEqual(result.project, self.project_name)
        self.assertEqual(result.resource_count, 5)

    def test_get_latest_update(self):
        """Test getting the latest update for a stack."""
        # Mock API response
        mock_response = {
            "updateId": "123456",
            "status": "succeeded",
            "timestamp": "2023-01-01T12:00:00Z",
        }
        self.mock_client._make_request.return_value = mock_response

        # Call the method
        result = self.stacks_resource.get_latest_update(self.org_name, self.project_name, self.stack_name)

        # Assertions
        self.mock_client._make_request.assert_called_once_with(
            "get",
            f"/api/stacks/{self.org_name}/{self.project_name}/{self.stack_name}/updates/latest",
        )
        self.assertEqual(result["updateId"], "123456")
        self.assertEqual(result["status"], "succeeded")

    def test_get_update(self):
        """Test getting a specific update for a stack."""
        update_id = "abc123"
        # Mock API response
        mock_response = {
            "updateId": update_id,
            "status": "succeeded",
            "timestamp": "2023-01-01T12:00:00Z",
        }
        self.mock_client._make_request.return_value = mock_response

        # Call the method
        result = self.stacks_resource.get_update(self.org_name, self.project_name, self.stack_name, update_id)

        # Assertions
        self.mock_client._make_request.assert_called_once_with(
            "get",
            f"/api/stacks/{self.org_name}/{self.project_name}/{self.stack_name}/updates/{update_id}",
        )
        self.assertEqual(result["updateId"], update_id)

    def test_list_tags(self):
        """Test listing tags for a stack."""
        # Mock API response
        mock_response = {"environment": "production", "owner": "team-a"}
        self.mock_client._make_request.return_value = mock_response

        # Call the method
        result = self.stacks_resource.list_tags(self.org_name, self.project_name, self.stack_name)

        # Assertions
        self.mock_client._make_request.assert_called_once_with(
            "get",
            f"/api/stacks/{self.org_name}/{self.project_name}/{self.stack_name}/tags",
        )
        self.assertEqual(result["environment"], "production")
        self.assertEqual(result["owner"], "team-a")

    def test_update_tags(self):
        """Test updating tags for a stack."""
        tags = {"environment": "staging", "team": "backend"}

        # Call the method
        self.stacks_resource.update_tags(self.org_name, self.project_name, self.stack_name, tags)

        # Assertions
        self.mock_client._make_request.assert_called_once_with(
            "patch",
            f"/api/stacks/{self.org_name}/{self.project_name}/{self.stack_name}/tags",
            data=tags,
        )

    def test_export_deployment(self):
        """Test exporting a stack deployment."""
        # Mock API response
        mock_response = {
            "version": 3,
            "deployment": {
                "resources": [
                    {"type": "aws:s3/bucket:Bucket", "name": "website"},
                    {"type": "aws:dynamodb/table:Table", "name": "data"},
                ]
            },
        }
        self.mock_client._make_request.return_value = mock_response

        # Call the method
        result = self.stacks_resource.export_deployment(self.org_name, self.project_name, self.stack_name)

        # Assertions
        self.mock_client._make_request.assert_called_once_with(
            "get",
            f"/api/stacks/{self.org_name}/{self.project_name}/{self.stack_name}/export",
        )
        self.assertEqual(result["version"], 3)
        self.assertEqual(len(result["deployment"]["resources"]), 2)


if __name__ == "__main__":
    unittest.main()
