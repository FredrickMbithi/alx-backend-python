#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient
Covers tasks 4 - 8
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for GithubOrgClient (tasks 4 - 7)
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Task 4:
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected URL.
        """
        client = GithubOrgClient(org_name)
        expected_url = f"https://api.github.com/orgs/{org_name}"
        client.org
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        Task 5:
        Test that _public_repos_url returns the expected result
        based on the mocked org payload.
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://some_url"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://some_url")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Task 6:
        Test that public_repos returns the expected list of repos
        and that the right calls are made.
        """
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "http://some_url"
            client = GithubOrgClient("test")
            result = client.public_repos()

            # Assert repos list matches expected
            self.assertEqual(result, ["repo1", "repo2"])

            # Assert mocks were called once
            mock_get_json.assert_called_once_with("http://some_url")
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Task 7:
        Test that has_license correctly returns True/False
        based on repo license key.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos (task 8)
    Using fixtures from fixtures.py
    """

    @classmethod
    def setUpClass(cls):
        """
        Start patcher for requests.get and set side_effect
        to return fixtures based on input URL.
        """
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith("orgs/test"):
                return MockResponse(cls.org_payload)
            elif url.endswith("repos"):
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stop patcher for requests.get
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Task 8:
        Test that public_repos returns the expected repos
        from the fixtures payload.
        """
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Task 8:
        Test that public_repos filters repos by license key
        using apache2_repos fixture.
        """
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


class MockResponse:
    """
    Simple mock response object to simulate requests.get().
    It returns a fixed payload when .json() is called.
    """

    def __init__(self, payload):
        """
        Initialize MockResponse with a payload that .json() will return.
        """
        self._payload = payload

    def json(self):
        """
        Return the stored payload as if it came from requests.get().json().
        """
        return self._payload


if __name__ == "__main__":
    unittest.main()
