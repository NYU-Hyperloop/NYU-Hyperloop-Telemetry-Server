# NYU-Hyperloop-Telemetry-Server
A secure telemetry server between the pod and an off-site server

## Setting up the server
Install Python 3 and PIP
```
// depends on platform
```

Install Flask:
```
pip3 install Flask
```

Install SocketIO:
```
pip3 install flask-socketio
```

Install Eventlet:
```
pip3 install eventlet
```

## Running the server

### Linux
```
export FLASK_APP=server.py
flask run
```

### Windows
```
set FLASK_APP=server.py
flask run
```

