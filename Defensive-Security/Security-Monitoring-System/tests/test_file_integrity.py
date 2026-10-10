import os
import tempfile
import unittest
from unittest.mock import patch

from detectors import file_integrity_monitor


class TestFileIntegrityMonitor(unittest.TestCase):

    def setUp(self):
        file_integrity_monitor.file_hashes.clear()
        file_integrity_monitor.missing_files.clear()

        self.temp_file = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(
            self.temp_file.name,
            "important.txt"
        )

        with open(self.file_path, "w") as file:
            file.write("Original content")

        file_integrity_monitor.register_file(self.file_path)

    def tearDown(self):
        self.temp_file.cleanup()

    @patch("detectors.file_integrity_monitor.create_alert")
    def test_file_modification(self, mock_alert):

        with open(self.file_path, "w") as file:
            file.write("Modified content")

        file_integrity_monitor.check_file(self.file_path)

        mock_alert.assert_called_once()

        self.assertEqual(
            mock_alert.call_args.args[0],
            "CRITICAL"
        )

    @patch("detectors.file_integrity_monitor.create_alert")
    def test_file_deletion_no_flooding(self, mock_alert):

        os.remove(self.file_path)

        for _ in range(5):
            file_integrity_monitor.check_file(self.file_path)

        mock_alert.assert_called_once()

        self.assertIn(
            self.file_path,
            file_integrity_monitor.missing_files
        )

    @patch("detectors.file_integrity_monitor.create_alert")
    def test_file_restoration(self, mock_alert):

        os.remove(self.file_path)

        file_integrity_monitor.check_file(self.file_path)

        with open(self.file_path, "w") as file:
            file.write("Restored content")

        file_integrity_monitor.check_file(self.file_path)

        self.assertEqual(mock_alert.call_count, 2)

        self.assertEqual(
            mock_alert.call_args.args[0],
            "INFO"
        )

        self.assertNotIn(
            self.file_path,
            file_integrity_monitor.missing_files
        )

    @patch("detectors.file_integrity_monitor.create_alert")
    def test_modification_after_restoration(self, mock_alert):

        # Step 1: Delete the file
        os.remove(self.file_path)
        file_integrity_monitor.check_file(self.file_path)

        # Step 2: Restore the file
        with open(self.file_path, "w") as file:
            file.write("Restored content")

        file_integrity_monitor.check_file(self.file_path)

        # Step 3: Modify the restored file
        with open(self.file_path, "w") as file:
            file.write("Modified after restoration")

        file_integrity_monitor.check_file(self.file_path)

        # Verify all three alerts
        self.assertEqual(mock_alert.call_count, 3)

        severities = [
            call.args[0]
            for call in mock_alert.call_args_list
        ]

        self.assertEqual(
            severities,
            ["CRITICAL", "INFO", "CRITICAL"]
        )