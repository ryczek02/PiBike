import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO
from app.utils.logger import log

socketio = SocketIO(cors_allowed_origins="*")
app = Flask(__name__)
socketio.init_app(app)

port=5000

@app.route('/')
def index():
    return "Sensor WebSocket Server"

@socketio.on('connect')
def on_connect():
    print("✅ Klient połączony")

@socketio.on('disconnect')
def on_disconnect():
    print("❌ Klient rozłączony")

def emit_data(data):
    with app.app_context():
        socketio.emit("sensor_data", data)

def run_socketio():
    log("FLASK:" + port)
    socketio.run(app, host="0.0.0.0", port=port)
