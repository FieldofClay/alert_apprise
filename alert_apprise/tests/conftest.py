# encoding = utf-8
"""
Shared pytest configuration for all tests.
"""
import pytest


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
