from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import Queue
import threading
import time
import ssl

import serial_device as serial
import fakeserial

# Serial input queue
serial_queue = Queue.Queue()

# Toggle on if testing
TESTING = True
if TESTING:
    # A fake "Arduino" serial for testing purposes
    arduino_serial = fakeserial.Serial(serial_queue)
else:
    arduino_serial = serial.Serial(serial_queue)

# Flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# SocketIO configuration
socketio = SocketIO(app, async_mode="gevent")

# Function that reads data from our serial input in a separate thread
def serve_data():
    while True:
        reading = serial_queue.get()
        with app.test_request_context('/'):
            socketio.emit('sensor_data', str(reading.data1))
            print("SEND TO CLIENT:", str(reading.data1))
        time.sleep(2)

# Default behavior on accessing the server
@app.route('/')
def index():
    return render_template("data.html")

# Triggered when a client connects to the server
@socketio.on('connect')
def handle_connect_event():
    print('Client connected')
    arduino_thread = threading.Thread(target=arduino_serial.read, name='Arduino-Read-Thread')
    data_thread = threading.Thread(target=serve_data, name='Data-Server-Thread')
    arduino_thread.daemon = True
    arduino_thread.start()
    data_thread.daemon = True
    data_thread.start()

# Triggered when a client disconnects from the server
@socketio.on('disconnect')
def handle_disconnect_event():
    print('Client disconnected')

# Triggered when the client sends the braking signal
@socketio.on('brake')
def handle_brake_event(message):
    if message["type"] == 'emergency':
        arduino_serial.write("Brake now!")

if __name__ == '__main__':
    # TODO: Current certificate and key are for testing purposes only
    socketio.run(app, host='127.0.0.1', port=8443, 
                        certfile='ssl/server/server.cer', keyfile='ssl/server/server.key', 
                        ca_certs='ssl/server/ca.cer', 
                        cert_reqs=ssl.CERT_REQUIRED,
                        ssl_version=ssl.PROTOCOL_TLSv1_2) 
    while True:
        time.sleep(1)

