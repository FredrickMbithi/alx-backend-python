#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @patch('client.get_json', return_value={"login": "holberton",
                                            "repos_url": "http://repos"})
    def test_org(self, mock_get_json):
        """Test that the org property returns expected JSON."""
        client = GithubOrgClient("holberton")
        result = client.org
        self.assertEqual(result, {"login": "holberton",
                                  "repos_url": "http://repos"})
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/holberton"
        )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct repo names."""
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = repos_payload

        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=Mock) as mock_url:
            mock_url.return_value = "http://repos"
            client = GithubOrgClient("holberton")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("http://repos")

    @parameterized.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False),
        ({}, "mit", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns True if license matches."""
        client = GithubOrgClient("holberton")
        self.assertEqual(client.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
