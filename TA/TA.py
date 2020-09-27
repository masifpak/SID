from Crypto.PublicKey import RSA
import socket

from Crypto.PublicKey import RSA


def TA_Key_Pair():
    secret = "searcindark"
    key = RSA.generate(2048)
    privatekey = key.exportKey(passphrase=secret, pkcs=8)
    publickey = key.publickey().exportKey()
    with open('TA_Private_key.pem', 'wb') as fpv:
        fpv.write(privatekey)
    with open('TA_Public_key.pem', 'wb') as fpub:
        fpub.write(publickey)
    #print privatekey
    #print publickey
TA_Key_Pair()

def TA_Listening():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 50002))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if not data:
            break
    conn.sendall(data)
    conn.close()