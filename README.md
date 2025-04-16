# PiBike 🚴‍♂️

**PiBike** is a modular, extensible **bike computer** built on Raspberry Pi.  
It collects real-time data from an **MPU6050 (accelerometer + gyroscope)** and a **GPS module**, logs it to a CSV file, and can optionally stream it over **WebSocket** using Flask-SocketIO.

## 🧩 Features

- ✅ Real-time data from MPU6050 (gyro + accel)
- ✅ Live GPS tracking (latitude, longitude, altitude, time)
- ✅ CSV logging with timestamps
- ✅ Optional WebSocket server for real-time streaming
- ✅ Feature flags via `.env` (enable/disable components)
- ✅ Modular & scalable architecture
- ✅ Auto-reconnect for GPS errors or disconnections

## ⚙️ Configuration (`.env`)

Create a `.env` file in the project root to configure what runs:

```ini
# Modules
USE_FLASK=true
USE_GYRO=true
USE_ACCEL=true
USE_GPS=true

# Sensors
SENSOR_DELAY=0.1
SERIAL_PORT=/dev/ttyS0
BAUD_RATE=115200

# Misc
TIMEZONE=Europe/Warsaw
```

## Installation 

Make sure you have Python 3.7+ and pip installed.

```bash
pip install -r requirements.txt
```

## ▶️ Running the Project

Run from the project root folder:

```bash
python3 -m app.main
```

## 📄 License

MIT License — use, modify, and enjoy 🚴‍♂️💻
