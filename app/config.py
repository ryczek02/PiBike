from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    "USE_FLASK": os.getenv("USE_FLASK", "false").lower() == "true",
    "USE_GYRO": os.getenv("USE_GYRO", "false").lower() == "true",
    "USE_ACCEL": os.getenv("USE_ACCEL", "false").lower() == "true",
    "USE_GPS": os.getenv("USE_GPS", "false").lower() == "true",
    "USE_KIVY": os.getenv("USE_KIVY", "false").lower() == "true",
    "SENSOR_DELAY": float(os.getenv("SENSOR_DELAY", "0.1")),
    "SERIAL_PORT": os.getenv("SERIAL_PORT", "/dev/ttyS0"),
    "BAUD_RATE": int(os.getenv("BAUD_RATE", "115200")),
    "TIMEZONE": os.getenv("TIMEZONE", "UTC"),
    
}
