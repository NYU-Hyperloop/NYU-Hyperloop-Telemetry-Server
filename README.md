# Secure-Telemetry-Server
A secure telemetry server between the pod and an off-site server

## Setting up the server
Install Python 2.7 and PIP (gevent-websocket does not fully support Python 3)

### Install required tools:
```
pip install pyserial
pip install Flask
pip install flask-socketio
pip install gevent
pip install gevent-websocket
```
### Install Client Certificate
Install `ssl/client/client.p12` on your OS or internet browser. Current password: `loop`.

## Running the server
**Do not run it using the `flask run` command. Use the following one instead:**
```
python server.py
```
The server runs at <https://127.0.0.1:8443>. 

## (Extras) (Not needed when testing server)

### Generating the SSL CA, Server Certificate and Client Certificate
```
sudo apt-get install openssl
openssl req -newkey rsa:4096 -keyform PEM -keyout ca.key -x509 -days 3650 -outform PEM -out ca.cer
openssl genrsa -out server.key 4096
openssl req -new -key server.key -out server.req -sha256
openssl x509 -req -in server.req -CA ca.cer -CAkey ca.key -set_serial 100 -extensions server -days 1460 -outform PEM -out server.cer -sha256
openssl genrsa -out client.key 4096
openssl req -new -key client.key -out client.req
openssl x509 -req -in client.req -CA ca.cer -CAkey ca.key -set_serial 101 -extensions client -days 365 -outform PEM -out client.cer
openssl pkcs12 -export -inkey client.key -in client.cer -out client.p12
rm server.req client.key client.cer client.req
```
