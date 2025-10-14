# encoding = utf-8
"""
Smoke tests for the helper module.
Tests validate the code structure without requiring dependencies.
"""
import os
import pytest


class TestHelperStructure:
    """Test helper module structure"""

    def test_helper_file_exists(self):
        """Test that the helper file exists"""
        helper_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "package", "bin", "alert_apprise", 
            "modalert_alert_apprise_helper.py"
        )
        assert os.path.exists(helper_path)

    def test_helper_has_process_event_function(self):
        """Test that helper defines process_event"""
        helper_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "package", "bin", "alert_apprise", 
            "modalert_alert_apprise_helper.py"
        )
        with open(helper_path, 'r') as f:
            content = f.read()
        assert 'def process_event' in content
        assert 'apprise' in content  # Uses apprise library
