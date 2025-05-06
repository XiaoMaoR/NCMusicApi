import os
import base64
import json
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

AESIV = "0102030405060708"
EAPIKEY = "e82ckenh8dichen8"
PRESETKEY = "0CoJUm6Qyw8W8jud"
LIUNXAPIKEY = "rFgB&h#%2?^eDg:Q"
BASE62= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
PUBLICKEY = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgtQn2JZ34ZC28NWYpAUd98iZ37BUrX/aKzmFbt7clFSs6sXqHauqKWqdtLkF2KexO40H1YTX8z2lSgBBOAxLsvaklV8k4cBFK9snQXE9/DDaFt6Rr7iVZMldczhC0JNgTz+SHXT6CBHuX3e9SdB1Ua44oncaTWz7OBGLbCiK45wIDAQAB\n-----END PUBLIC KEY-----"

def rsaEncrypt(data, public_key=PUBLICKEY):
    rsa_public_key = serialization.load_pem_public_key(
        public_key.encode('utf-8'),
        backend=default_backend()
    )
    if not isinstance(rsa_public_key, rsa.RSAPublicKey):
        raise ValueError("Provided key is not an RSA public key")
    if isinstance(data, str):
        data = data.encode('utf-8')
    key_size = rsa_public_key.key_size // 8
    if len(data) > key_size:
        raise ValueError(f"Data too long for RSA key size ({len(data)} > {key_size})")
    padded_data = b'\x00' * (key_size - len(data)) + data

    numbers = rsa_public_key.public_numbers()
    e = numbers.e
    n = numbers.n

    m = int.from_bytes(padded_data, byteorder='big')
    c = pow(m, e, n)
    encrypted = c.to_bytes(key_size, byteorder='big')
    return encrypted

def pkcs7_pad(data, block_size=16):
    padding_length = block_size - (len(data) % block_size)
    return data + bytes([padding_length] * padding_length)

def pkcs7_unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

def random_string(length=16):
    return ''.join(BASE62[b % 62] for b in os.urandom(length))

def aesEncrypt(data, mode, key, iv):
    if isinstance(data, str):
        data = data.encode('utf-8')
    if mode == 'cbc':
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    elif mode == 'ecb':
        cipher = Cipher(algorithms.AES(key), modes.ECB())
    else:
        raise ValueError("Unsupported mode: {}".format(mode))
    encryptor = cipher.encryptor()
    padded_data = pkcs7_pad(data)
    return encryptor.update(padded_data) + encryptor.finalize()

def linuxapi(data):
    text = json.dumps(data)
    encrypted = aesEncrypt(
        text.encode(),
        'ecb',
        LIUNXAPIKEY.encode(),
        b''
    )
    return {
        'eparams': encrypted.hex().upper()
    }

def weapi(data):
    text = json.dumps(data)
    secretKey = [ord(BASE62[b % 62]) for b in os.urandom(16)]
    encrypted = aesEncrypt(
        base64.b64encode(aesEncrypt(text.encode(), 'cbc', PRESETKEY.encode(), AESIV.encode())),
        'cbc',
        bytes(secretKey),
        AESIV.encode()
    )
    return {
        'params': base64.b64encode(encrypted).decode(),
        'encSecKey': rsaEncrypt(bytes(secretKey[::-1]), PUBLICKEY).hex()
    }

def eapi(url, data):
    text = json.dumps(data) if isinstance(data, dict) else str(data)
    message = f'nobody{url}use{text}md5forencrypt'
    digest = hashlib.md5(message.encode()).hexdigest()
    data = f'{url}-36cd479b6b5-{text}-36cd479b6b5-{digest}'
    encrypted = aesEncrypt(
        data.encode(),
        'ecb',
        EAPIKEY.encode(),
        b''
    )
    return {
        'params': encrypted.hex().upper()
    }

def aesDecrypt(cipher_buffer, key, mode='ecb', iv=b''):
    if mode == 'cbc':
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    elif mode == 'ecb':
        cipher = Cipher(algorithms.AES(key), modes.ECB())
    else:
        raise ValueError("Unsupported mode: {}".format(mode))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(cipher_buffer) + decryptor.finalize()
    return pkcs7_unpad(decrypted)

def decrypt(cipher_buffer):
    return aesDecrypt(cipher_buffer, EAPIKEY.encode())