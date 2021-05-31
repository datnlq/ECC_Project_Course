#!/bin/env python3.6

from tinyec import registry
from Crypto.Cipher import AES
import hashlib, binascii,base64,secrets
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad



#AES
def encrypt_AES_CBC(msg, AES_key):
    AES_cipher = AES.new(AES_key, AES.MODE_CBC)
    ct_bytes = AES_cipher.encrypt(pad(msg, AES.block_size))
    iv = base64.b64encode(AES_cipher.iv).decode('utf-8')
    c = base64.b64encode(ct_bytes).decode('utf-8')
    return c,iv

def decrypt_AES_CBC(ciphertext, iv , secretKey):
    AES_Cipher = AES.new(secretKey, AES.MODE_CBC, iv)
    plaintext = AES_Cipher.decrypt(ciphertext)
    return plaintext



#ECC


def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext


def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

curve = registry.get_curve('brainpoolP256r1')

def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)

def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext


if __name__ == '__main__':
    msg = b"Nguyen Le Quoc Dat"
          
    print("Original msg:", msg)
    AES_key = get_random_bytes(16) #128bit
    print("AES_key = ",AES_key)
    AES_c , AES_iv = encrypt_AES_CBC(msg,AES_key)
    print("AES_cipher = ",AES_c)
    print("AES_iv = ",AES_iv)
    AES_iv = base64.b64decode(AES_iv)
    ECC_plaintext = base64.b64decode(AES_c)
    print("ECC_plaintext = ",ECC_plaintext)

    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g

    ECC_cipher = encrypt_ECC(ECC_plaintext, pubKey)
    encryptedMsgObj = {
        'ciphertext': binascii.hexlify(ECC_cipher[0]),
        'nonce': binascii.hexlify(ECC_cipher[1]),
        'authTag': binascii.hexlify(ECC_cipher[2]),
        'ciphertextPubKey': hex(ECC_cipher[3].x) + hex(ECC_cipher[3].y % 2)[2:]
        }
    print("encrypted msg:", encryptedMsgObj)

    ECC_plain = decrypt_ECC(ECC_cipher, privKey)
    #ECC_plaint = base64.b64decode(ECC_plain)
    #print("decrypted msg:", ECC_plaint)
    AES_plaintext = decrypt_AES_CBC(ECC_plain,AES_iv,AES_key)
    print(AES_plaintext)

