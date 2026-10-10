import unittest
from datetime import datetime
from unittest.mock import patch

from detectors import network_detector


class TestNetworkDetector(unittest.TestCase):

    def setUp(self):
        network_detector.connection_attempts.clear()
        network_detector.last_alert_time.clear()

    @patch("detectors.network_detector.create_alert")
    def test_port_scan_detection(self, mock_alert):

        ip_address = "192.168.1.50"

        connections = [
            ("13:00:01", 22),
            ("13:00:05", 80),
            ("13:00:10", 443)
        ]

        for time_string, port in connections:
            timestamp = datetime.strptime(
                time_string, "%H:%M:%S"
            )

            network_detector.process_connection(
                ip_address,
                port,
                timestamp,
                port_threshold=3,
                time_window=60
            )

        mock_alert.assert_called_once()

    @patch("detectors.network_detector.create_alert")
    def test_port_scan_cooldown(self, mock_alert):

        ip_address = "192.168.1.50"

        connections = [
            ("13:00:01", 22),
            ("13:00:05", 80),
            ("13:00:10", 443),
            ("13:00:15", 3306),
            ("13:00:20", 8080)
        ]

        for time_string, port in connections:
            timestamp = datetime.strptime(
                time_string, "%H:%M:%S"
            )

            network_detector.process_connection(
                ip_address,
                port,
                timestamp,
                port_threshold=3,
                time_window=60
            )

        mock_alert.assert_called_once()


    @patch("detectors.network_detector.create_alert")
    def test_below_threshold(self, mock_alert):

        ip_address = "192.168.1.50"

        connections = [
            ("13:00:01", 22),
            ("13:00:05", 80)
        ]

        for time_string, port in connections:
            timestamp = datetime.strptime(
                time_string, "%H:%M:%S"
            )

            network_detector.process_connection(
                ip_address,
                port,
                timestamp,
                port_threshold=3,
                time_window=60
            )

        mock_alert.assert_not_called()



    @patch("detectors.network_detector.create_alert")
    def test_connections_outside_time_window(self, mock_alert):

        ip_address = "192.168.1.50"

        connections = [
            ("13:00:00", 22),
            ("13:02:00", 80),
            ("13:04:00", 443)
        ]

        for time_string, port in connections:

            timestamp = datetime.strptime(
                time_string, "%H:%M:%S"
            )

            network_detector.process_connection(
                ip_address,
                port,
                timestamp,
                port_threshold=3,
                time_window=60
            )

        mock_alert.assert_not_called()



    
    @patch("detectors.network_detector.process_connection")
    @patch("builtins.print")
    def test_invalid_ip_address(self, mock_print, mock_process):

        line = "13:00:01 999.999.999.999 22"

        network_detector.process_network_log_line(
            line,
            port_threshold=3,
            time_window=60
        )

        mock_process.assert_not_called()
        mock_print.assert_called_once()


    @patch("detectors.network_detector.process_connection")
    @patch("builtins.print")
    def test_invalid_port_number(self, mock_print, mock_process):

        line = "13:00:01 192.168.1.50 70000"

        network_detector.process_network_log_line(
            line,
            port_threshold=3,
            time_window=60
        )

        mock_process.assert_not_called()
        mock_print.assert_called_once()


    @patch("detectors.network_detector.process_connection")
    @patch("builtins.print")
    def test_invalid_timestamp(self, mock_print, mock_process):

        line = "INVALID_TIME 192.168.1.50 22"

        network_detector.process_network_log_line(
            line,
            port_threshold=3,
            time_window=60
        )

        mock_process.assert_not_called()
        mock_print.assert_called_once()

