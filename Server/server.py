from Crypto.PublicKey import RSA


def Server_Key_Pair():
    secret = "searcindark"
    key = RSA.generate(2048)
    privatekey = key.exportKey(passphrase=secret, pkcs=8)
    publickey = key.publickey().exportKey()
    with open('Server_Private_key.pem', 'wb') as fpv:
        fpv.write(privatekey)
    with open('Server_Public_key.pem', 'wb') as fpub:
        fpub.write(publickey)
    #print privatekey
    #print publickey
Server_Key_Pair()


def Server_Listening():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 50001))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
    conn.close()