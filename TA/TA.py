from Crypto.PublicKey import RSA
#code = 'searcindark'

#key = RSA.generate(2048)
#privatekey = key.exportKey(passphrase=code, pkcs=8)
#publickey = key.publickey().exportKey()

#print privatekey
#print publickey

import socket

def Ta_Listening():
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))
s.listen(1)
conn, addr = s.accept()
while 1:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)
conn.close()