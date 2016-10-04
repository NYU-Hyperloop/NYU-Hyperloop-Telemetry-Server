openssl genrsa -out client.key 4096
openssl req -new -key client.key -out client.req -subj "/C=US/ST=New-York/L=New-York/O=NYU-Hyperloop/CN=$1"
openssl x509 -req -in client.req -CA server/ca.cer -CAkey server/ca.key -set_serial 101 -extensions client -days 365 -outform PEM -out client.cer
openssl pkcs12 -export -inkey client.key -in client.cer -out client.p12
cp client.p12 client/client_$1.p12
rm client.key client.cer client.req client.p12
echo 'New client certificate generated'