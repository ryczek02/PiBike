import pytest
from unittest.mock import patch, MagicMock
from app.sensors.gps_l76g import GPS

@patch("app.sensors.gps_l76g.serial.Serial")
@patch("app.sensors.gps_l76g.pynmea2.parse")
def test_gps_read(mock_parse, mock_serial):
    gps = GPS()
    
    mock_serial_instance = MagicMock()
    mock_serial_instance.is_open = True
    mock_serial_instance.readline.return_value = b"$GNGGA,TEST"
    mock_serial.return_value = mock_serial_instance

    mock_msg = MagicMock()
    mock_msg.latitude = 50.0
    mock_msg.longitude = 20.0
    mock_msg.timestamp.strftime.return_value = "12:00:00"
    mock_parse.return_value = mock_msg

    with patch("builtins.print"), patch("time.sleep"):  # suppress output & delay
        result = gps.read()

    assert result == {
        "gps_lat": 50.0,
        "gps_lon": 20.0,
        "gps_time": "12:00:00"
    }
