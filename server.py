from flask import Flask, Response, redirect, request, render_template
from flask_socketio import SocketIO, send, emit
import threading
import fakeserial as serial
import time
import eventlet

# Eventlet configuration
eventlet.monkey_patch()

# Flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# SocketIO configuration
socketio = SocketIO(app, async_mode="eventlet")

# A fake "Arduino" serial for testing purposes
arduino_serial = serial.Serial(0)

# Function that reads data from our serial input in a separate thread
def read_from_arduino():
    global arduino_serial
    while True:
        reading = arduino_serial.readline()
        with app.test_request_context('/'):
            socketio.emit('sensor_data', reading)
            print("SEND TO CLIENT:",reading)
        time.sleep(2)

# Default behavior on accessing the server
@app.route('/')
def index():
    return render_template("data.html")

# Triggered when a client connects to the server
@socketio.on('connect')
def handle_connect_event():
    print('Client connected')
    arduino_thread = threading.Thread(target=read_from_arduino, name='Arduino-Read-Thread')
    arduino_thread.start()

# Triggered when a client disconnects from the server
@socketio.on('disconnect')
def handle_disconnect_event():
    print('Client disconnected')

# Triggered when the client sends the braking signal
@socketio.on('brake')
def handle_brake_event(message):
    if message["type"] == 'emergency':
        print('Emergency brake initiated')
        arduino_serial.write("Brake now!")

if __name__ == '__main__':
    socketio.run(app)