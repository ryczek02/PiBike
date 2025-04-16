from .mpu6050 import MPU6050
from .gps import GPS
from app.config import CONFIG

def get_enabled_sensors():
    sensors = []
    mpu = MPU6050()

    if CONFIG["USE_GYRO"] or CONFIG["USE_ACCEL"]:
        sensors.append(mpu)
    if CONFIG["USE_GPS"]:
        sensors.append(GPS())

    return sensors
