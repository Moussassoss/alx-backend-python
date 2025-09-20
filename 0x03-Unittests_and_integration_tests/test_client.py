#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean value"""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([{
    "org_payload": TEST_PAYLOAD[0][0],
    "repos_payload": TEST_PAYLOAD[0][1],
    "expected_repos": TEST_PAYLOAD[0][2],
    "apache2_repos": TEST_PAYLOAD[0][3],
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch client.get_json so no real HTTP requests happen"""
        cls.get_patcher = patch("client.get_json")
        cls.mock_get_json = cls.get_patcher.start()

        # return different payloads based on the URL passed
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                return cls.repos_payload
            return None

        cls.mock_get_json.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patch after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license"""
        client = GithubOrgClient("google")
        result = client.public_repos(license_key="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
