openssl req -newkey rsa:4096 -keyform PEM -keyout ca.key -x509 -days 3650 -outform PEM -out ca.cer -subj '/C=US/ST=New-York/L=New-York/O=NYU-Hyperloop/CN=NYU-Hyperloop-Telemetry/emailAddress=nyu@hyper.loop'
openssl genrsa -out server.key 4096
openssl req -new -key server.key -out server.req -sha256 -subj '/C=US/ST=New-York/L=New-York/O=NYU-Hyperloop/CN=localhost'
openssl x509 -req -in server.req -CA ca.cer -CAkey ca.key -set_serial 100 -extensions server -days 1460 -outform PEM -out server.cer -sha256
openssl genrsa -out client.key 4096
openssl req -new -key client.key -out client.req -subj '/C=US/ST=New-York/L=New-York/O=NYU-Hyperloop/CN=127.0.0.1'
openssl x509 -req -in client.req -CA ca.cer -CAkey ca.key -set_serial 101 -extensions client -days 365 -outform PEM -out client.cer
openssl pkcs12 -export -inkey client.key -in client.cer -out client.p12
cp ca.cer server/ca.cer
cp ca.key server/ca.key
cp server.cer server/server.cer
cp server.key server/server.key
cp client.p12 client/client_127.0.0.1.p12
rm server.req client.key client.cer client.req ca.cer ca.key server.cer server.key client.p12
echo 'SSL configuration complete'