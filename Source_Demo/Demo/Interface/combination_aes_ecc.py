#library for aes

import aes, os

from Crypto.Cipher import AES

#library for ecc

from ecc.curve import Curve25519, Point

from ecc.key import gen_keypair

from ecc.cipher import ElGamal

from Crypto.Util.number import *
import sqlite3
from sqlite3 import Error



BLOCK_SIZE = 16

file_name = "ECCapp.db"



def padding(text):

    return text + b"\0" * (BLOCK_SIZE - len(text) % BLOCK_SIZE)



def encrypt_aes(text):

    key = os.urandom(BLOCK_SIZE)

    iv = os.urandom(BLOCK_SIZE)

    aes = AES.new(key, AES.MODE_CBC, iv)

    enc = aes.encrypt(text)

    return enc, key, iv



def encrypt_ecc(text):

    # Generate key pair

    pri_key, pub_key = gen_keypair(Curve25519)

    # Encrypt using ElGamal algorithm

    cipher_elg = ElGamal(Curve25519)

    C1, C2 = cipher_elg.encrypt(text, pub_key)

    return pri_key,pub_key, C1, C2



def decrypt_ecc(pri_key, C1, C2):

    cipher_elg = ElGamal(Curve25519)

    new_plaintext = cipher_elg.decrypt(pri_key, C1, C2)

    return new_plaintext



def decrypt_aes(cipher_text, key, iv):

    aess = AES.new(key, AES.MODE_CBC, iv)

    new_plaintext = aess.decrypt(cipher_text)



    return new_plaintext



def Pointtrans(F):
    a = F
    b = a.split("X=")
    c = b[1].split(',')
    x = c[0]
    d = c[1].split(',')
    e = d[0].split("Y=")
    y = e[1]
    return  x,y
if __name__ == "__main__":

    try:
        db = sqlite3.connect("Server.db")
        curr = db.cursor()
    except Error as e:
        print(e)

    with open(file_name, "rb") as fi:
        text = fi.read()
    text = padding(text)
    #aes encrypt 

    AES_cipher , AES_key, AES_iv = encrypt_aes(text)

    #ecc encrypt aes's key

    pri_key, pub_key, C1, C2 = encrypt_ecc(AES_key)
    C1_x,C1_y = Pointtrans(str(C1))
    C2_x,C2_y = Pointtrans(str(C2))
    Publickey_x,Publickey_y = Pointtrans(str(pub_key))
    AEScipher = bytes_to_long(AES_cipher)
    AESiv = bytes_to_long(AES_iv)
    # print(C1_x)
    # print(C1_y)
    # print(C2_x)
    # print(C2_y)
    # print(Publickey_x)
    # print(Publickey_y)
    # print(AEScipher)
    # print(AESiv)
    server_update = (C1_x,C1_y,C2_x,C2_y,Publickey_x,Publickey_y,str(AEScipher),str(AESiv),1)

    sql = ''' UPDATE SERVER
              SET C1_x = ? ,
                  C1_y = ? ,
                  C2_x = ? ,
                  C2_y = ? ,
                  Publickey_x = ? ,
                  Publickey_y = ? ,
                  AES_cipher = ? ,
                  AES_iv = ?
              WHERE ID = ?
        '''
    curr = db.cursor()
    curr.execute(sql, server_update)
    db.commit()
    try:
        conn = sqlite3.connect("ECCapp.db")
        cur = conn.cursor()
        # print(sqlite3.version)
    except Error as e:
        print(e)
    sql = ''' UPDATE TEACHER
              SET PrivateKey = ? 
              WHERE TeacherID = ?
              '''
    teacher = (str(pri_key),'anv')
    cur = conn.cursor()
    cur.execute(sql,teacher)
    conn.commit()


    print("Encrypt done ! ")

#-------------------------------------------------
    print("Decrypt Beginning!")


    curr.execute("SELECT * FROM SERVER WHERE ID=?", (1,))
    rs = curr.fetchone()
    #print(rs[1])
    C1_x = int(rs[1])
    C1_y = int(rs[2])
    C2_x = int(rs[3])
    C2_y = int(rs[4])
    AES_cipher = long_to_bytes(int(rs[7]))
    AES_iv = long_to_bytes(int(rs[8]))
    db.commit()
    cur.execute("SELECT * FROM TEACHER WHERE TeacherID=?", ('anv',))
    th = cur.fetchone()
    pri_key = th[6]

    print(C1_x)
    print(C1_y)
    print(C2_x)
    print(C2_y)
    print(Publickey_x)
    print(Publickey_y)
    print(AEScipher)
    print(AESiv)
    print(pri_key)
    # decrypt

    C1 = Point(C1_x, C1_y, curve=Curve25519)
    C2 = Point(C2_x, C2_y, curve=Curve25519)

    new_ECC_plainkey = decrypt_ecc(pri_key, C1, C2)

    new_plaintext = decrypt_aes(AES_cipher, new_ECC_plainkey, AES_iv)



    o = open('output.db','wb')
    o.write(new_plaintext)
    o.close()