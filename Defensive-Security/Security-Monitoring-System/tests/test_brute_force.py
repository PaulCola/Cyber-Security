import unittest
from datetime import datetime
from unittest.mock import patch

from detectors import brute_force_detector


class TestBruteForceDetector(unittest.TestCase):

    def setUp(self):
        brute_force_detector.failed_attempts.clear()
        brute_force_detector.last_alert_time.clear()

    @patch("detectors.brute_force_detector.create_alert")
    def test_brute_force_detection(self, mock_alert):

        ip_address = "192.168.1.25"

        timestamps = [
            datetime.strptime("13:00:01", "%H:%M:%S"),
            datetime.strptime("13:00:05", "%H:%M:%S"),
            datetime.strptime("13:00:10", "%H:%M:%S")
        ]

        for timestamp in timestamps:
            brute_force_detector.process_failed_login(
                ip_address,
                timestamp,
                threshold=3,
                time_window=60
            )

        mock_alert.assert_called_once()

    @patch("detectors.brute_force_detector.create_alert")
    def test_brute_force_cooldown(self, mock_alert):

        ip_address = "192.168.1.25"

        timestamps = [
            datetime.strptime("13:00:01", "%H:%M:%S"),
            datetime.strptime("13:00:05", "%H:%M:%S"),
            datetime.strptime("13:00:10", "%H:%M:%S"),
            datetime.strptime("13:00:15", "%H:%M:%S"),
            datetime.strptime("13:00:20", "%H:%M:%S")
        ]

        for timestamp in timestamps:
            brute_force_detector.process_failed_login(
                ip_address,
                timestamp,
                threshold=3,
                time_window=60
            )

        mock_alert.assert_called_once()


    @patch("detectors.brute_force_detector.create_alert")
    def test_below_threshold(self, mock_alert):

        ip_address = "192.168.1.25"

        timestamps = [
            datetime.strptime("13:00:01", "%H:%M:%S"),
            datetime.strptime("13:00:05", "%H:%M:%S")
        ]

        for timestamp in timestamps:
            brute_force_detector.process_failed_login(
                ip_address,
                timestamp,
                threshold=3,
                time_window=60
            )

        mock_alert.assert_not_called()



    @patch("detectors.brute_force_detector.create_alert")
    def test_attempts_outside_time_window(self, mock_alert):

        ip_address = "192.168.1.25"

        timestamps = [
            datetime.strptime("13:00:00", "%H:%M:%S"),
            datetime.strptime("13:02:00", "%H:%M:%S"),
            datetime.strptime("13:04:00", "%H:%M:%S")
        ]

        for timestamp in timestamps:
            brute_force_detector.process_failed_login(
                ip_address,
                timestamp,
                threshold=3,
                time_window=60
            )

        mock_alert.assert_not_called()



   



    @patch("detectors.brute_force_detector.process_failed_login")
    @patch("builtins.print")
    def test_invalid_ip_address(self, mock_print, mock_process):

        line = (
            "Oct 09 13:00:01 server sshd[1234]: "
            "Failed password for admin from "
            "999.999.999.999 port 50121 ssh2"
        )

        brute_force_detector.process_log_line(
            line,
            threshold=3,
            time_window=60
        )

        mock_process.assert_not_called()
        mock_print.assert_called_once()


    @patch("detectors.brute_force_detector.process_failed_login")
    @patch("builtins.print")
    def test_missing_ip_address(self, mock_print, mock_process):

        line = (
            "Oct 09 13:00:01 server sshd[1234]: "
            "Failed password for admin from"
        )

        brute_force_detector.process_log_line(
            line,
            threshold=3,
            time_window=60
        )

        mock_process.assert_not_called()
        mock_print.assert_called_once()


    @patch("detectors.brute_force_detector.process_failed_login")
    @patch("builtins.print")
    def test_invalid_timestamp(self, mock_print, mock_process):

        line = (
            "Oct 09 INVALID_TIME server sshd[1234]: "
            "Failed password for admin from "
            "192.168.1.25 port 50121 ssh2"
        )

        brute_force_detector.process_log_line(
            line,
            threshold=3,
            time_window=60
        )

        mock_process.assert_not_called()
        mock_print.assert_called_once()