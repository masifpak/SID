
from Crypto.PublicKey import RSA
import os
import hashlib
import hmac
import base64
from cryptography.fernet import Fernet
import random
import cPickle as pickle
import math
import array
import string
from Crypto.Cipher import AES

class SIDClient:

    '''
    a=[0,1]
    b=[0,1]
    spk=5
    spx=2
    X=[]
    import itertools

    K=list(itertools.product([0,1], repeat=spk))
    print K
    X=list(itertools.product([0,1], repeat=spx))
    print X

    def logical_xor(str1, str2):
        print logical_xor(str1,str2)
        logical_xor(k,x)

    #######################
    '''



    def Client_Key_Pair():
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

    Client_Key_Pair()

    def KG():
        """
        Generates a key and save it into a file
        """
        x = os.urandom(128)
        k = os.urandom(16)
        #print x
        #print k
        K_G = x + k
        #print KG
        KG = base64.b64encode(K_G)
        print "KG: " , KG
        with open("secret.key", "wb") as key_file:
            key_file.write(KG)
            return KG
    KG()
    #def exportkeys():
    #    # print self.K1, self.K2, self.K3, self.K4
    #    return KG

    def load_key():
        """
        Load the previously generated key
        """

        return open("secret.key", "rb").read()

    def Generate_KSE():
        AES_key_length = 32  # use larger value in production
        secret_key = os.urandom(AES_key_length)
        KSE = base64.b64encode(secret_key)
        file = open('KSE.key', 'wb')
        file.write(KSE)
        file.close()
        print "KSE: " ,  KSE
        return KSE
    #y = Generate_KSE()
     # def Final_K (self):
   #     KSE = Generate_KSE()
   #     KG  = KG()
   #     Final_K = KG + KSE
    #    print Final_K
    #    return final_K

    #    Final_K()

    def G(self, kg, data):
        hash = hashlib.sha256(kg + data)
        G = hash.digest()
        #print G.encode('hex')
        return G

        #while 2 * self.addr_size > len(G):
        #G += hash.update(self.K2).digest()
        # print G[:2 * self.addr_size]   ## Nothing print
        #return G[:2 * self.addr_size]

    def H(self, kw, data):
        #hash = hashlib.sha512(data)
        m = hmac.new(kw)
        m.update(data)
        addr = m.hexdigest()

        #addr = hash.digest()
        # while length > len(Hx):
        #     hash.update(data)
        #     Hx += hash.digest()
        #return Hx[:length]
        return addr


    #def H(self, data):
    #    print self.Hx(data, self.id_size + self.addr_size)
    #    return self.Hx(data, self.id_size + self.addr_size)

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
    #ENC (y, 'I love pakistan to much')

    def File_ENC (self, KSE, filename):
        f = Fernet(KSE)
        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()
            CFi = f.encrypt(file_data)
            return CFi

    def __init__(self, k = 32, z = 100000):
        self.k = k
        self.z = z
        self.kse = 0
        self.id_size = 20       # SHA1 is used for file ID and is 20 bytes long. Currently not changeable
        self.addr_size = 0
    Generate_KSE()
