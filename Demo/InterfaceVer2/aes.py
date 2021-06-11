import aes, os 
from Crypto.Cipher import AES

BLOCK_SIZE = 16
file_name = "zlatan.hehe"

def encrypt_aes(text):
    text = text + b"\0" * (BLOCK_SIZE -  len(text) % BLOCK_SIZE)
    key = os.urandom(BLOCK_SIZE)
    iv = os.urandom(BLOCK_SIZE)
    aes = AES.new(key, AES.MODE_CBC, iv)
    enc = aes.encrypt(text)
    return enc

if __name__ == "__main__":
    with open(file_name, "rb") as fi:
        text = fi.read()
    print(encrypt_aes(text))