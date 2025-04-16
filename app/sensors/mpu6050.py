import smbus2
from .base_sensor import BaseSensor

MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
ACCEL_XOUT_H = 0x3B

GYRO_SENSITIVITY = 131.0
ACCEL_SENSITIVITY = 16384.0

class MPU6050(BaseSensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        self.bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

    def read_word(self, reg):
        high = self.bus.read_byte_data(MPU6050_ADDR, reg)
        low = self.bus.read_byte_data(MPU6050_ADDR, reg + 1)
        value = (high << 8) + low
        return value - 65536 if value >= 0x8000 else value

    def read(self):
        gx = self.read_word(GYRO_XOUT_H) / GYRO_SENSITIVITY
        gy = self.read_word(GYRO_XOUT_H + 2) / GYRO_SENSITIVITY
        gz = self.read_word(GYRO_XOUT_H + 4) / GYRO_SENSITIVITY
        ax = self.read_word(ACCEL_XOUT_H) / ACCEL_SENSITIVITY
        ay = self.read_word(ACCEL_XOUT_H + 2) / ACCEL_SENSITIVITY
        az = self.read_word(ACCEL_XOUT_H + 4) / ACCEL_SENSITIVITY

        return {
            "gyro_x": gx,
            "gyro_y": gy,
            "gyro_z": gz,
            "accel_x": ax,
            "accel_y": ay,
            "accel_z": az
        }
