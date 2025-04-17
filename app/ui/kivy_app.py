from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from app.config import CONFIG
from threading import Thread
import time

# Zmienna globalna do odbioru danych
sensor_data = {}

class SensorScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.status_label = Label(font_size='24sp')
        self.data_label = Label(font_size='20sp')
        self.add_widget(self.status_label)
        self.add_widget(self.data_label)
        Clock.schedule_interval(self.update_labels, 0.5)

    def update_labels(self, dt):
        status = f"SocketIO: {'ON' if CONFIG['USE_FLASK'] else 'OFF'}"
        data_lines = [f"{k}: {v}" for k, v in sensor_data.items()]
        self.status_label.text = status
        self.data_label.text = "\n".join(data_lines)

class SensorApp(App):
    def build(self):
        Window.fullscreen = True
        return SensorScreen()

def start_kivy():
    SensorApp().run()

def update_sensor_data_loop():
    from app.sensors.sensor_factory import get_enabled_sensors
    sensors = get_enabled_sensors()

    while True:
        combined = {}
        for sensor in sensors:
            try:
                reading = sensor.read()
                if reading:
                    combined.update(reading)
            except Exception as e:
                print("[KIVY SENSOR ERROR]", e)

        global sensor_data
        sensor_data = combined
        time.sleep(CONFIG["SENSOR_DELAY"])
