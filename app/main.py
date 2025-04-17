import threading
import time
from .config import CONFIG
from .sensors.sensor_factory import get_enabled_sensors
from .services.csv_logger import log_to_csv
from app.utils.logger import log  # jeśli używasz naszego loggera

if CONFIG["USE_FLASK"]:
    from app.server.socket_server import emit_data, run_socketio

shared_data = {}
data_lock = threading.Lock()

def sensor_worker(sensor):
    sensor_name = sensor.__class__.__name__
    while True:
        try:
            data = sensor.read()
            if data:
                with data_lock:
                    shared_data.update(data)
        except Exception as e:
            log(f"Błąd w sensorze {sensor_name}: {e}", level="ERROR")
        time.sleep(CONFIG["SENSOR_DELAY"])

def emit_loop():
    while True:
        time.sleep(CONFIG["SENSOR_DELAY"])
        with data_lock:
            data_copy = shared_data.copy()

        if data_copy:
            log_to_csv(data_copy)
            if CONFIG["USE_FLASK"]:
                emit_data(data_copy)

if __name__ == "__main__":
    sensors = get_enabled_sensors()

    for sensor in sensors:
        threading.Thread(target=sensor_worker, args=(sensor,), daemon=True).start()

    threading.Thread(target=emit_loop, daemon=True).start()

    # Startuj socketio jeśli trzeba
    if CONFIG["USE_FLASK"]:
        run_socketio()
    else:
        while True:
            time.sleep(1)
