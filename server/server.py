import socket
from cryptography.hazmat.primitives.asymmetric import rsa, dh
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

with open("server_public.pem", "wb") as f:
    f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))

s = socket.socket()
s.bind(("0.0.0.0", 1234)) 
s.listen(1)

conn, addr = s.accept()

client_public_key = serialization.load_pem_public_key(conn.recv(4096))
with open("server_public.pem", "rb") as f:
    conn.sendall(f.read())

parameters = dh.generate_parameters(generator=2, key_size=2048)
dh_private_key = parameters.generate_private_key()
dh_public_key = dh_private_key.public_key()

client_dh_public_key = serialization.load_pem_public_key(conn.recv(4096))
conn.sendall(dh_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))

shared_key = dh_private_key.exchange(client_dh_public_key)
derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data').derive(shared_key)

data = conn.recv(4096)
iv = data[:16]
ciphertext = data[16:]

cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

padding_length = plaintext[-1]
plaintext = plaintext[:-padding_length]

with open("received_file.txt", "wb") as f:
    f.write(plaintext)

conn.close()
