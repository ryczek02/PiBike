import pytest
from unittest.mock import MagicMock, patch
from app.sensors.accel_gyro_mpu_6050 import MPU6050

@patch("app.sensors.accel_gyro_mpu_6050.smbus2.SMBus")
def test_mpu6050_read(mock_smbus):
    mock_bus = MagicMock()
    # 0x7FFF = 32767, simulating max value
    mock_bus.read_byte_data.side_effect = [0x7F, 0xFF] * 6
    mock_smbus.return_value = mock_bus

    sensor = MPU6050()
    data = sensor.read()

    # Check that all expected keys are returned
    assert all(k in data for k in ["gyro_x", "gyro_y", "gyro_z", "accel_x", "accel_y", "accel_z"])
    # Assert float values
    assert isinstance(data["gyro_x"], float)
