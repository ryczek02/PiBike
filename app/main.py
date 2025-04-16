import threading
import time
from .config import CONFIG
from .sensors.sensor_factory import get_enabled_sensors
from .services.csv_logger import log_to_csv

if CONFIG["USE_FLASK"]:
    from app.server.socket_server import emit_data, run_socketio

def sensor_loop():
    sensors = get_enabled_sensors()

    while True:
        combined_data = {}
        for sensor in sensors:
            data = sensor.read()
            if data:
                combined_data.update(data)

        log_to_csv(combined_data)

        if CONFIG["USE_FLASK"]:
            emit_data(combined_data)

        time.sleep(CONFIG["SENSOR_DELAY"])

if __name__ == "__main__":
    threading.Thread(target=sensor_loop, daemon=True).start()

    if CONFIG["USE_FLASK"]:
        run_socketio()
    else:
        while True:
            time.sleep(1)
