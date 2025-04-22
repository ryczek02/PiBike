from app.sensors.sensor_factory import get_enabled_sensors
from unittest.mock import patch

@patch("app.sensors.sensor_factory.CONFIG", {"USE_GYRO": True, "USE_ACCEL": False, "USE_GPS": True})
@patch("app.sensors.sensor_factory.MPU6050")
@patch("app.sensors.sensor_factory.GPS")
def test_get_enabled_sensors(mock_gps, mock_mpu):
    sensors = get_enabled_sensors()
    assert any(isinstance(s, mock_mpu.return_value.__class__) for s in sensors)
    assert any(isinstance(s, mock_gps.return_value.__class__) for s in sensors)
