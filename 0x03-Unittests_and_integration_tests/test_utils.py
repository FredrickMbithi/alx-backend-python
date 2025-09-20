#!/usr/bin/env python3
"""Integration tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient


@parameterized_class([
    {
        "org_payload": {"login": "holberton", "repos_url": "http://repos"},
        "repos_payload": [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}}
        ],
        "expected_repos": ["repo1", "repo2", "repo3"],
        "license_key": None,
        "expected_repos_license": ["repo1", "repo3"]
    }
])
class TestGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @patch("client.get_json")
    def test_org(self, mock_get_json):
        """Test org property returns the expected dictionary."""
        mock_get_json.return_value = self.org_payload
        client = GithubOrgClient("holberton")
        result = client.org
        self.assertEqual(result, self.org_payload)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/holberton"
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct list of repository names."""
        mock_get_json.return_value = self.repos_payload
        client = GithubOrgClient("holberton")

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=Mock) as mock_url:
            mock_url.return_value = "http://repos"
            result = client.public_repos()
            self.assertEqual(result, self.expected_repos)
            mock_get_json.assert_called_once_with("http://repos")

    @patch("client.get_json")
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos filters repos by license."""
        mock_get_json.return_value = self.repos_payload
        client = GithubOrgClient("holberton")

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=Mock) as mock_url:
            mock_url.return_value = "http://repos"
            result = client.public_repos(license="mit")
            self.assertEqual(result, self.expected_repos_license)
            mock_get_json.assert_called_once_with("http://repos")

    @parameterized_class.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False),
        ({}, "mit", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license static method returns correct boolean."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
