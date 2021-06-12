#library for aes
import aes, os 
from Crypto.Cipher import AES
#library for ecc
from ecc.curve import Curve25519
from ecc.key import gen_keypair
from ecc.cipher import ElGamal

BLOCK_SIZE = 16
file_name = "zlatan.hehe"

def encrypt_aes(text):
    text = text + b"\0" * (BLOCK_SIZE -  len(text) % BLOCK_SIZE)
    key = os.urandom(BLOCK_SIZE)
    iv = os.urandom(BLOCK_SIZE)
    aes = AES.new(key, AES.MODE_CBC, iv)
    enc = aes.encrypt(text)
    return enc

def encrypt_ecc(text):
    # Generate key pair
    pri_key, pub_key = gen_keypair(Curve25519)
    # Encrypt using ElGamal algorithm
    cipher_elg = ElGamal(Curve25519)
    C1, C2 = cipher_elg.encrypt(text, pub_key)

    # Decrypt
    new_plaintext = cipher_elg.decrypt(pri_key, C1, C2) # check

    print("private: ", pri_key)
    print("public: ", pub_key)
    print(C1)
    print(C2)

if __name__ == "__main__":
    with open(file_name, "rb") as fi:
        text = fi.read()
    encrypt_ecc(encrypt_aes(text))