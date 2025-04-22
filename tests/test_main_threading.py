import threading
from app.sensors.base_sensor import BaseSensor
from app.main import sensor_worker, shared_data, data_lock

class MockSensor(BaseSensor):
    def read(self):
        return {"test": 123}

def test_sensor_worker_thread():
    sensor = MockSensor()
    thread = threading.Thread(target=sensor_worker, args=(sensor,), daemon=True)
    thread.start()
    # Give thread time to run
    import time; time.sleep(0.2)

    with data_lock:
        assert "test" in shared_data
