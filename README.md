# Secure-Telemetry-Server
A secure telemetry server between the pod and an off-site server

## Setting up the server
Install Python 2.7 and PIP (gevent-websocket does not fully support Python 3)

### Install required tools:
```
pip install pyserial Flask flask-socketio gevent gevent-websocket
```
### Configure SSL connection
- Install `ssl/client/client.p12` on your OS or internet browser. Development password: `loop`.
- Install `ssl/client/greenlock.p7b` as a **Trusted Root Certification Authority** on your OS or internet browser.

## Running the server
**Do not run it using the `flask run` command. Use the following one instead:**
```
python server.py
```
The server runs at <https://localhost:8443>.
**If accessed via 127.0.0.1, there will be a domain mismatch with the SSL certificate.**

## (Extras) (Not needed when testing server)
### Generating the SSL Certification Authority, Server Certificate and Client Certificate
```
cd ssl
./configure.sh
```
### Getting the browser to recognize the Certification Authority (Obtaining 'Green Lock')
- Tutorial designed for Google Chrome
1. Navigate to <https://localhost:8443>.
2. Click on the broken lock in the URL bar -> Details -> View Certificate
3. Go to Certification Path and find the untrusted certificate (should be the root) -> View Certificate
4. Go to Details -> Copy to File -> export as a P7B and choose the location
5. Install the P7B
..* Go to chrome://settings -> Advanced -> HTTPS/SSL -> Manage Certificates
..* Import the P7B file under Trusted Root Certification Authority
..* Restart the browser
