openssl genrsa -out server.key 4096
openssl req -new -key server.key -out server.req -sha256 -subj "/C=US/ST=New-York/L=New-York/O=NYU-Hyperloop/CN=$1"
openssl x509 -req -in server.req -CA server/ca.cer -CAkey server/ca.key -CAcreateserial -CAserial herong.seq -extensions server -days 1460 -outform PEM -out server.cer -sha256
cp server.cer server/server.cer
cp server.key server/server.key
rm server.req server.cer server.key
echo 'Server IP updated.'