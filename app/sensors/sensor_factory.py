from .accel_gyro_mpu_6050 import MPU6050
from .gps_l76g import GPS
from app.config import CONFIG

def get_enabled_sensors():
    sensors = []
    mpu = MPU6050()

    if CONFIG["USE_GYRO"] or CONFIG["USE_ACCEL"]:
        sensors.append(mpu)
    if CONFIG["USE_GPS"]:
        sensors.append(GPS())

    return sensors
