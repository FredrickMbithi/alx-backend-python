#!/usr/bin/env python3
"""Unit tests for utils.py.

Covers:
- access_nested_map (valid + exceptions)
- get_json (mocked requests)
- memoize decorator
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Tests for utils.access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Return correct value for valid paths."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        """Raise KeyError with the right message for invalid paths."""
        with self.assertRaises(KeyError) as cm:
            utils.access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), expected_msg)


class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Return JSON payload and call requests.get once."""
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = test_payload
            result = utils.get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self):
        """a_method should be called once and result cached."""

        class TestClass:
            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass, "a_method", return_value=42
        ) as mock_method:
            obj = TestClass()

            # first access triggers a_method
            self.assertEqual(obj.a_property, 42)

            # second access should use cached value
            self.assertEqual(obj.a_property, 42)

            mock_method.assert_called_once()
