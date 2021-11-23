#!/usr/bin/env python3
import socket
# ==================================================
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import binascii

# ==================================================

# default 
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8888        # The port used by the server
cmd_GET_MENU = b"GET_MENU"
cmd_END_DAY = b"CLOSING"
default_menu = "menu_today.txt"
menu_file = "menu.csv"
return_file = "day_end.csv"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    my_socket.connect((HOST, PORT))
    my_socket.sendall(cmd_GET_MENU )
    data = my_socket.recv(4096)

    # Decrypting data with private key ===============
    with open('mykeyMenu.pem','r') as f:
        keyPair = RSA.import_key(f.read())
    decryptor = PKCS1_OAEP.new(keyPair)
    dataDecrypted = decryptor.decrypt(data)
    print('Decrypted:', dataDecrypted.decode('utf8'))
    # ================================================

    # Verfiying signature with public key ============
    with open ('pubkeyDS.pem', 'r') as x:
        pubkeyDS = x.read()
    pubkey = RSA.importKey(pubkeyDS)
    signer = pkcs1_15.new(pubkey)
    with open ('signature.csv', 'rb') as s:
        signature = s.read()
        
    digest = SHA256.new(data)

    # Uncomment to print out digest and signature to verify it matches with server side

    # print("\nDigest:")
    # for b in digest.digest():
    #     print("{0:02x}".format(b),end="")
    # print("\n")
    # print("\nSignature:")
    # for b in signature:
    #     print("{0:02x}".format(b),end="")

    try:
        signer.verify(digest,signature)
        print("\nVerifying signature...")
        print("\nThe signature is valid\n")
    except (ValueError, TypeError):
        print ("\nThe signature is not valid.")


    #   ================================================
    menu_file = open(menu_file,"wb")
    menu_file.write(data)
    menu_file.close()
    my_socket.close()
# return hexadecimal representation of binary data, 
# each byte of data is converted into 2 digit hex representation 
print('Received', repr(data))  # for debugging use
my_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    my_socket.connect((HOST, PORT))
    my_socket.sendall(cmd_END_DAY)
    out_file = open(return_file,"rb")

    # Generating RSA keypair for day_end file =============
    keyPairDE = RSA.generate(2048)
    with open('myKeyDE.pem','wb') as f:
        f.write(keyPairDE.export_key('PEM'))
    
    pubkeyDE = keyPairDE.publickey()

    # Encrypting day_end file =============================
    file_bytes = out_file.read(1024)
    encryptor = PKCS1_OAEP.new(pubkeyDE)
    encrypted = encryptor.encrypt(file_bytes)
    print("\nEncrypted:", binascii.hexlify(encrypted))
    # ======================================================
    my_socket.send(encrypted)

    out_file.close()
    my_socket.close()
print('\nSent', repr(encrypted))  # for debugging use
my_socket.close()
