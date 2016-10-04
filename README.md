# Secure-Telemetry-Server
A secure telemetry server for sending data and receiving commands from the pod to an off-site client

## Setting up the server
Install Python 2.7 and PIP

### Install required tools:
```
pip install pyserial Flask flask-socketio gevent gevent-websocket
```
### Configure SSL connection
- Install `ssl/client/client_YOUR_CLIENT_IP.p12` on your OS or internet browser. Development password: `loop`.
- Install `ssl/client/greenlock.p7b` as a **Trusted Root Certification Authority** on your OS or internet browser.

## Running the server
**Do not run it using the `flask run` command. Use the following one instead:**
```
python server.py
```
The server runs at <https://localhost:8443>. Testing username and password: 'hyper' - 'loop'
**If accessed via 127.0.0.1, there will be a domain mismatch with the SSL certificate.**

## (Extras) (Not needed when testing server)
### Generating the SSL Certification Authority, Server Certificate and default Client Certificate
```
cd ssl
./initial_setup.sh
```
### Updating the server IP to make it accessible from the network
```
cd ssl
sh update_server_ip.sh NEW_SERVER_IP
```
### Generating a client certificate for a new client
```
cd ssl
sh new_client.sh CLIENT_IP
```
### Getting the browser to recognize the Certification Authority (Obtaining 'Green Lock')
Tutorial designed for Google Chrome on Windows, settings may slightly vary for other OS's and browsers

1. Navigate to <https://localhost:8443>.
2. Click on the broken lock in the URL bar -> Details -> View Certificate
3. Go to Certification Path and find the untrusted certificate (should be the root) -> View Certificate
4. Go to Details -> Copy to File -> export as a P7B and choose the location
5. Install the P7B
  * Go to chrome://settings -> Advanced -> HTTPS/SSL -> Manage Certificates
  * Import the P7B file under Trusted Root Certification Authority
  * Restart the browser
