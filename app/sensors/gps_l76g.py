import serial
import pynmea2
from .base_sensor import BaseSensor
from app.config import CONFIG
import time

class GPS(BaseSensor):
    def __init__(self):
        self.ser = None

    def read(self):
        while True:
            try:
                if self.ser is None or not self.ser.is_open:
                    self.ser = serial.Serial(CONFIG["SERIAL_PORT"], CONFIG["BAUD_RATE"], timeout=None)

                line = self.ser.readline()
                if line:
                    decoded = line.decode('ascii', errors='replace').strip()
                    if decoded.startswith('$GNGGA'):
                        try:
                            msg = pynmea2.parse(decoded)
                            return {
                                "gps_lat": msg.latitude,
                                "gps_lon": msg.longitude,
                                "gps_time": msg.timestamp.strftime("%H:%M:%S")
                            }
                        except pynmea2.ParseError:
                            continue
            except Exception as e:
                print("[GPS] Błąd GPS:", e)
                if self.ser:
                    try:
                        self.ser.close()
                    except:
                        pass
                self.ser = None
                time.sleep(2)
