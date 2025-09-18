#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        result = client.org  # access property, do not call it

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct URL from org payload"""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        client = GithubOrgClient("google")

        with patch.object(
                GithubOrgClient,
                "org",
                new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names"""
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = payload

        client = GithubOrgClient("google")
        fake_url = "https://api.github.com/orgs/google/repos"

        with patch.object(
                GithubOrgClient,
                "_public_repos_url",
                new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = fake_url

            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]

            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(fake_url)


if __name__ == "__main__":
    unittest.main()
