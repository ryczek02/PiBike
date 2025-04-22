import os
from unittest.mock import patch, mock_open
from app.services import csv_logger

@patch("builtins.open", new_callable=mock_open)
def test_log_to_csv(mock_file):
    data = {
        "gyro_x": 1.0, "gyro_y": 2.0, "gyro_z": 3.0,
        "accel_x": 4.0, "accel_y": 5.0, "accel_z": 6.0,
        "gps_lat": 50.0, "gps_lon": 20.0, "gps_time": "12:00:00"
    }
    csv_logger.log_to_csv(data)
    mock_file.assert_called()  # file opened
