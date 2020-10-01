
from Crypto.PublicKey import RSA
import os
import hashlib
import hmac
import base64
from cryptography.fernet import Fernet
import socket
from Crypto.Cipher import AES

class SIDClient:

    def Client_Key_Pair(self):
        secret = "searcindark"
        key = RSA.generate(2048)
        privatekey = key.exportKey(passphrase=secret, pkcs = 8)
        publickey = key.publickey().exportKey()
        with open('Client_Private_key.pem', 'wb') as fpv:
            fpv.write(privatekey)
        with open('Client_Public_key.pem', 'wb') as fpub:
            fpub.write(publickey)
        #print privatekey
        #print publickey


    ''' KG is the key for Invertible PRF'''
    def KG(self):
        """
        Generates a key and save it into a file
        """
        x = os.urandom(128)
        k = os.urandom(16)
        K_G = x + k
        #print KG
        KG = base64.b64encode(K_G)
        #print "KG: " , KG
        with open("secret.key", "wb") as key_file:
            key_file.write(KG)
            return KG

    ''' KSE is a Symmetric Key for Cloud Service Provider (CSP)'''
    def Generate_KSE(self):
        AES_key_length = 32  # use larger value in production
        secret_key = os.urandom(AES_key_length)
        KSE = base64.b64encode(secret_key)
        file = open('KSE.key', 'wb')
        file.write(KSE)
        file.close()
        #print "KSE: " ,  KSE
        return KSE

    ''' G (KG,  h(wij)||no. of searches (wij)) '''
    def G(self, kg, data):
        hash = hashlib.sha256(kg + data)
        G = hash.digest()
        #print G.encode('hex')
        return G

    ''' This is Keyed Hash Function for taking hash of Word key and conncatenated message  '''
    def H(self, kw, data):
        #hash = hashlib.sha512(data)
        m = hmac.new(kw)
        m.update(data)
        addr = m.hexdigest()
        return addr

    ''' Encryption function for encrypted value'''
    def ENC (self, KSE, msg):
        iv = os.urandom(16)
        sec_key = base64.b64decode(KSE)
        # use the decoded secret key to create a AES cipher
        cipher = AES.new(sec_key, AES.MODE_CFB, iv)
        #cipher = AES.new(self.K4, AES.MODE_CFB, iv)
        #pad_msg = msg + (padding * ((16 - len(msg)) % 16))
        noofiles_conc_fileid = msg
        encrypted_msg = cipher.encrypt(noofiles_conc_fileid)
        encoded_enc_msg = base64.b64encode(encrypted_msg)
        # return encoded encrypted message
        #print encoded_enc_msg
        return encoded_enc_msg

    ''' Encryption Function for Files'''
    def File_ENC (self, KSE, filename):
        f = Fernet(KSE)
        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()
            CFi = f.encrypt(file_data)
            return CFi

    ''' Encryption Function for Word'''
    def hash_word(self, w):
        #hash_w = hashlib.sha511(w)
        hash_w = (hashlib.sha512(w)).digest()
        return hash_w

    ''' Generating ID of files'''
    def file_id (self, filename):
        f_id = id(filename)
        return f_id

    ''' Cleaning CSV files'''
    def clean(self):
        ## To empty CSV files for each turn
        f = open('allwords-counts.csv', 'w')
        f.truncate(0)
        f = open('file_count_index.csv', 'w')
        f.truncate(0)
        f = open('search_word_index.csv', 'w')
        f.truncate(0)
        f = open('add-val-map.csv', 'w')
        f.truncate(0)

    '''
    def client_socket():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('0.0.0.0', 50002))
        client.send("I am CLIENT<br>")
        from_server = client.recv(4095)
        client.close()
        print from_server
    client_socket()
    '''