import socket
from cryptography.hazmat.primitives.asymmetric import rsa, dh
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

with open("client_public.pem", "wb") as f:
    f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))

s = socket.socket()
s.connect(("server", 1234))  

with open("client_public.pem", "rb") as f:
    s.sendall(f.read())

server_public_key = serialization.load_pem_public_key(s.recv(4096))

parameters = dh.generate_parameters(generator=2, key_size=2048)
dh_private_key = parameters.generate_private_key()
dh_public_key = dh_private_key.public_key()

s.sendall(dh_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
server_dh_public_key = serialization.load_pem_public_key(s.recv(4096))

shared_key = dh_private_key.exchange(server_dh_public_key)
derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data').derive(shared_key)

iv = os.urandom(16)
cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
encryptor = cipher.encryptor()

with open("file.txt", "rb") as f:
    plaintext = f.read()

padding_length = 16 - (len(plaintext) % 16)
plaintext += bytes([padding_length] * padding_length)
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

s.sendall(iv + ciphertext)
s.close()
