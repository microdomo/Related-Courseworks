import datetime

# ==================================================
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import binascii
from rbac import RBAC
# ==================================================

cmd_GET_MENU = "GET_MENU"
cmd_END_DAY = "CLOSING"
default_menu = "menu_today.txt"
default_save_base = "result-"

def process_connection( conn , ip_addr, MAX_BUFFER_SIZE):
    blk_count = 0
    net_bytes = conn.recv(MAX_BUFFER_SIZE)

    dest_file = open("temp","w")
    while net_bytes != b'':
        if blk_count == 0: #  1st block
            usr_cmd = net_bytes[0:15].decode("utf8").rstrip()
            if cmd_GET_MENU in usr_cmd: # ask for menu
                src_file = open(default_menu,"rb")

                # Generate RSA keypair for menu =========================
                keyPair = RSA.generate(2048)
                with open('mykeyMenu.pem', 'wb') as f:
                    f.write(keyPair.export_key('PEM'))

                pubKey = keyPair.publickey()
                # =======================================================

                # Generating RSA keypair for DS =========================
                keyPairDS = RSA.generate(2048)
                privatekey = keyPairDS.export_key('PEM')
                with open ('mykeyDS.pem', 'wb') as y:
                    y.write(privatekey)

                pubkeyDS = keyPairDS.publickey()

                with open ('pubkeyDS.pem', 'wb') as x:
                    x.write(pubkeyDS.export_key('PEM'))

                while True:
                    # Encrypting menu with public key ================
                    read_bytes = src_file.read(MAX_BUFFER_SIZE)
                    encryptor = PKCS1_OAEP.new(pubKey)
                    encrypted = encryptor.encrypt(read_bytes)
                    print("\nEncrypted:", binascii.hexlify(encrypted))
                    # ================================================

                    # Digital Signature ==============================
                    digest = SHA256.new(encrypted)
                    print("\nDigest: ")
                    for b in digest.digest():
                        print("{0:02x}".format(b),end="")

                    print("\n\nSignature:")
                    signature = pkcs1_15.new(keyPairDS).sign(digest)
                    with open ('signature.csv','wb') as s:
                        s.write(signature)
                        for b in signature:
                            print("{0:02x}".format(b),end="")
                    # ================================================
                    conn.send(encrypted)

                    if read_bytes == b'':
                        break
                    break
                src_file.close()
                print("\n\nProcessed SENDING menu")
                return
            elif cmd_END_DAY in usr_cmd: # ask for to save end day order
                now = datetime.datetime.now()
                filename = default_save_base +  ip_addr + "-" + now.strftime("%Y-%m-%d_%H%M")
                dest_file = open(filename,"wb")
                net_bytes = conn.recv(MAX_BUFFER_SIZE)

                # Decrypting data with private key ===============
                with open('mykeyDE.pem','r') as f:
                    keyPairDE = RSA.import_key(f.read())
                decryptor = PKCS1_OAEP.new(keyPairDE)
                dataDecrypted = decryptor.decrypt(net_bytes)
                print('\nDecrypted:', dataDecrypted.decode('utf8'))
                # ================================================
                dest_file.write(dataDecrypted)  # remove the CLOSING header
                blk_count = blk_count + 1
                print('\nReceived', repr(dataDecrypted))

        else:  # write other blocks
            net_bytes = conn.recv(MAX_BUFFER_SIZE)
            dest_file.write(net_bytes)
    # last block / empty block
    # print('Received', repr(net_bytes))
    dest_file.close()
    print("\nProcessed CLOSING done")


def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    process_connection( conn, ip, MAX_BUFFER_SIZE)
    conn.close()  # close connection
    print('Connection ' + ip + ':' + port + " ended")

def start_server():

    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind(("127.0.0.1", 8888))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        print( msg.with_traceback() )
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()

def rbac():
    # Flat RBAC Implementation =======================================================================
    rbac = RBAC()
    #   Role for junior employee at SPAM2 Server
    jr_employee = rbac.create_role('jr_employee')

    #   Resources such as data files on SPAM2 server
    data_files = rbac.create_domain('data_files')

    #   Create read permission
    read = rbac.create_permission('r')

    #   Give junior employees read permission for data files, do not have rights to write or modify 
    jr_employee.add_permission(read, data_files)

    #   Create a subject. a user or a third party client
    new_employee = rbac.create_subject('new')

    #   New employee
    new_employee.authorize(jr_employee)

    #   lock rbac configuration so that no unauthorised user can change configuration
    rbac.lock()

    #   Check will raise an exception since user does not have permission
    # rbac.go(user not part of rbac, data_files, read)
    # raised RBACAuthorizationError
    # ===============================================================================================


rbac()
start_server()

