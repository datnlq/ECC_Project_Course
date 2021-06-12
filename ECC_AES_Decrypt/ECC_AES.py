import aes, os
from Crypto.Cipher import AES
#library for ecc
from ecc.curve import Curve25519, Point
from ecc.key import gen_keypair
from Crypto.Util.number import*
from ecc.cipher import ElGamal
import sqlite3
from sqlite3 import Error







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

    #-------------------------------------------------
    # print("Decrypt Beginning!")


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

    print("C1_x = ",C1_x)
    print("C1_y = ",C1_y)
    print("C2_x = ",C2_x)
    print("C2_y = ",C2_y)
    # print(Publickey_x)
    # print(Publickey_y)
    print("AES_cipher = " ,bytes_to_long(AES_cipher))
    print("AES_iv = " ,bytes_to_long(AES_iv))
    # print(pri_key)
    # decrypt
    try:
        conn = sqlite3.connect("teacherkey.db")
        cur = conn.cursor()
        # print(sqlite3.version)
    except Error as e:
        print(e)


    cur.execute("SELECT * FROM TEACHER WHERE TeacherID=?", ('anv',))
    th = cur.fetchone()
    pri_key = int(th[2])
    print("PrivateKey = " ,pri_key)
    conn.close()


    C1 = Point(C1_x, C1_y, curve=Curve25519)
    C2 = Point(C2_x, C2_y, curve=Curve25519)

    new_ECC_plainkey = decrypt_ecc(pri_key, C1, C2)

    new_plaintext = decrypt_aes(AES_cipher, new_ECC_plainkey, AES_iv)

    

    o = open('Capp.db','wb')
    o.write(new_plaintext)
    o.close()
    