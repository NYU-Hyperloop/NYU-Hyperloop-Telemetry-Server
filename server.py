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
import os
import sys

import fakeserial
import serverconfig

# Flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'q-7g{D3(^T!t]e/y'

# Toggle on if testing
parser = argparse.ArgumentParser(description='Telemetry server')
parser.add_argument('-t', action='store_true')
parser.add_argument('-d', action='store_true')
args = parser.parse_args()

serverconfig = serverconfig.ServerConfig('server.cfg', args.t)

# Suppress errors in order to ignore the SSLEOFError until we find a fix
# WARNING: THIS IS BAD. Comment it out in order to see the errors.
#f = open(os.devnull, 'w')
#sys.stderr = f


# Serial input queue
serial_queue = Queue.Queue()

arduino_serial = serverconfig.Serial(serial_queue)

if args.d:
    app.debug = True

# SocketIO configuration
socketio = SocketIO(app, async_mode='gevent')

# We should keep track of our clients and only serve data once
serving_data = False
clients = 0

# Function that reads data from our serial input in a separate thread
def serve_data():
    global serving_data
    while serving_data:
        reading = serial_queue.get()
        with app.test_request_context('/'):
            socketio.emit('sensor_data', reading)
            print('SEND TO CLIENT:', reading)
            print('\n')
        time.sleep(2)

# Default behavior on accessing the server
@app.route('/')
def index():
    return render_template('data.html')

# Triggered when a client connects to the server
@socketio.on('connect')
def handle_connect_event():
    global serving_data
    global clients
    clients += 1
    print('LOG: Client connected. Total: ' + str(clients) + '\n')
    time.sleep(2) # We need to give our thread enough time to exit. Otherwise, a page refresh keeps starting new threads.
    if not serving_data:
        serving_data = True
        arduino_thread = threading.Thread(target=arduino_serial.read, name='Arduino-Read-Thread')
        data_thread = threading.Thread(target=serve_data, name='Data-Server-Thread')
        arduino_thread.start()
        data_thread.start()

# Triggered when a client disconnects from the server
@socketio.on('disconnect')
def handle_disconnect_event():
    global serving_data
    global clients
    clients -= 1
    print('LOG: Client disconnected. Total: ' + str(clients) + '\n')
    if clients == 0:
        serving_data = False

# Triggered when the client sends a command
@socketio.on('command')
def handle_gui_command(command):
    # TODO: Send the actual commands that Arduino would expect
    arduino_serial.write(command);

if __name__ == '__main__':
    # TODO: Current certificate and key are for testing purposes only
    socketio.run(app, host=serverconfig.host, port=serverconfig.port,
                      certfile=serverconfig.certfile, keyfile=serverconfig.keyfile,
                      ca_certs=serverconfig.ca_certs,
                      cert_reqs=ssl.CERT_REQUIRED,
                      ssl_version=ssl.PROTOCOL_TLSv1_2) 

    while True:
        time.sleep(1)

