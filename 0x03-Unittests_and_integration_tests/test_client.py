#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected, mock_get_json):
        """Test GithubOrgClient.org returns correct payload"""
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        #!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected, mock_get_json):
        """Test GithubOrgClient.org returns correct payload"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        with patch("client.GithubOrgClient.org",
                   new_callable=unittest.mock.PropertyMock) as mock_org:
            # Mock .org to return this fake payload
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/testorg/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        # Fake payload returned by get_json
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        # Mock the _public_repos_url property
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=unittest.mock.PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Assertions
            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
from parameterized import parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""
        cls.get_patcher = patch("requests.get")

        # Start the patch
        mock_get = cls.get_patcher.start()

        # Configure side_effect for .json() based on URL
        def side_effect(url):
            mock_response = unittest.mock.Mock()
            if url.endswith("/orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


