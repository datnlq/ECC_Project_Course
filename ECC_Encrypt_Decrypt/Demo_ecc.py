#!/bin/env python3

from tinyec import registry
from Crypto.Cipher import AES
import hashlib, binascii,base64,secrets
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


#AES
def encrypt_AES_CBC(msg, AES_key):
    cipher = AES.new(AES_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(msg, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    c = base64.b64encode(ct_bytes).decode('utf-8')
    return c,iv

def decrypt_AES_CBC(ciphertext, nonce, authTag, secretKey):
    AES_Cipher = AES.new(secretKey, AES.MODE_CBC, nonce)
    plaintext = AES_Cipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext



#ECC
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
    ECC_plaintext = base64.b64decode(AES_c)
    print("ECC_plaintext = ",ECC_plaintext)


    privateKey = secrets.randbelow(curve.field.n)
    publicKey = privKey * curve.g

    encryptedMsg = encrypt_ECC(ECC_plaintext, publicKey)
    encryptedMsgObj = {
        'ciphertext': binascii.hexlify(encryptedMsg[0]),
        'nonce': binascii.hexlify(encryptedMsg[1]),
        'authTag': binascii.hexlify(encryptedMsg[2]),
        'ciphertextpublicKey': hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:]
    }
    print("Encrypted msg:", encryptedMsgObj)

    decryptedMsg = decrypt_ECC(encryptedMsg, privateKey)
    print("Decrypted msg:", decryptedMsg)#!/bin/env python3

from tinyec import registry
from Crypto.Cipher import AES
import hashlib, binascii,base64,secrets
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


#AES
def encrypt_AES_CBC(msg, AES_key):
    cipher = AES.new(AES_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(msg, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    c = base64.b64encode(ct_bytes).decode('utf-8')
    return c,iv

def decrypt_AES_CBC(ciphertext, nonce, authTag, secretKey):
    AES_Cipher = AES.new(secretKey, AES.MODE_CBC, nonce)
    plaintext = AES_Cipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext



#ECC
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
    ECC_plaintext = base64.b64decode(AES_c)
    print("ECC_plaintext = ",ECC_plaintext)


    privateKey = secrets.randbelow(curve.field.n)
    publicKey = privKey * curve.g

    encryptedMsg = encrypt_ECC(ECC_plaintext, publicKey)
    encryptedMsgObj = {
        'ciphertext': binascii.hexlify(encryptedMsg[0]),
        'nonce': binascii.hexlify(encryptedMsg[1]),
        'authTag': binascii.hexlify(encryptedMsg[2]),
        'ciphertextpublicKey': hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:]
    }
    print("Encrypted msg:", encryptedMsgObj)

    decryptedMsg = decrypt_ECC(encryptedMsg, privateKey)
    print("Decrypted msg:", decryptedMsg)