from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

# Necessary to make standard library cooperate with gevent
from gevent import monkey
monkey.patch_all()

import argparse
import Queue
import threading
import time
import ssl

import fakeserial
import ServerConfig

# Flask configuration
app = Flask(__name__)

# Toggle on if testing
parser = argparse.ArgumentParser(description='Telemetry server')
parser.add_argument('-t', action='store_true')
parser.add_argument('-d', action='store_true')
args = parser.parse_args()

serverconfig = ServerConfig.ServerConfig('server.cfg', args.t)

# Serial input queue
serial_queue = Queue.Queue()

arduino_serial = serverconfig.Serial(serial_queue)

if args.d:
    app.debug = True

app.config['SECRET_KEY'] = serverconfig.get('Flask', 'SECRET_KEY')

# SocketIO configuration
socketio = SocketIO(app, async_mode="gevent")

# Function that reads data from our serial input in a separate thread
def serve_data():
    while True:
        reading = serial_queue.get()
        print str(reading.int_sensor)
        with app.test_request_context('/'):
            socketio.emit('sensor_data', str(reading.int_sensor))
            print("SEND TO CLIENT:", str(reading.int_sensor))
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
    socketio.run(app, host=serverconfig.host, port=serverconfig.port,
                      certfile=serverconfig.certfile, keyfile=serverconfig.keyfile,
                      ca_certs=serverconfig.ca_certs,
                      cert_reqs=ssl.CERT_REQUIRED,
                      ssl_version=ssl.PROTOCOL_TLSv1_2) 

    while True:
        time.sleep(1)
