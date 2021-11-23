import socket
import json
import datetime

print("\nConnecting to client...")

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('0.0.0.0', 8089))
serversocket.listen(5) # maximum 5 connections, handle one at a time
connection, address = serversocket.accept()

# Datetime module
def sub_years(date,year):
    return date.replace(year= date.year + year)
start_date = datetime.date.today()

# Receive name of user logged in from client
def recvname(con):
    while True:
        buf = con.recv(255) # buf is of the type of byte
        if len(buf) > 0:
            # To change ' to " for json to work
            loggedinuser = buf.decode()
            with open ("loggedinuser.json","w") as x:
                json.dump(loggedinuser,x,indent=3)
            break
        else: #0 length buf implies client has dropped the con.
            return "" # quit this handler immediately and return ""  
    # con.close()
    return buf.decode()

# Receive the amount of times user bought a service from client
def recvnum(con):
    while True:
        buf = con.recv(255)
        if len(buf) > 0:
            nbuf = buf.decode()
            with open('repeat.json','w') as u:
                u.write(nbuf)
                brepeat = json.dumps(nbuf)
                brepeat = brepeat.replace("'","")
                brepeat = brepeat.replace("\"","")
                global repeat
                repeat = brepeat.strip('][').split(', ')
            break
        break
    return buf.decode()

# Receive the services user bought from client
def recvsubs(con):
    while True:
        buf = con.recv(255)
        if len(buf) > 0:
            print("\nReceiving user's newly bought subscriptions...")
            with open('loggedinuser.json') as u:
                loggedinuser = json.load(u)
            with open("services.json") as x:
                services_dict = json.load(x)
            # To change string back to list
            buser_cart = buf.decode()
            buser_cart = buser_cart.replace("'","")
            user_cart = buser_cart.strip('][').split(', ')
            with open(f"{loggedinuser}.txt",'a') as f:
                for i in range(0, len(repeat)): 
                    repeat[i] = int(repeat[i])
                for i in range(len(repeat)):
                    times = repeat[i]
                    global end_date
                    end_date = sub_years(start_date,times)
                    f.write(f"\n{i+1}. {user_cart[i]}: ${services_dict[user_cart[i]]}k/year \nSubscription Start Date: {start_date}\nSubscription End Date: {end_date}\n")
    return buf.decode()

# Receive new user account created from client
def recvlogin(con):
    while True:
        buf = con.recv(255) # buf is of the type of byte
        if len(buf) > 0:
            print("\nUpdating file for any changes made...")
            # To change ' to " for json to work
            json_acceptable_string = (buf.decode()).replace("'", "\"")
            newuserlogin = json.loads(json_acceptable_string)
            with open ("users.json","w") as x:
                json.dump(newuserlogin,x,indent=3)
            with open("users.json","r") as y:
                users_dict = json.load(y)
                for i in users_dict:
                    with open(f'{i}.txt','w') as u:
                        u.write(f"{i}'s susbcriptions \n")
            break
            # if buf == b"q" or buf == b"X":
            #     break              
            # else:
                # con.sendall(buf) # echo back the same byte sequence to client
        else: #0 length buf implies client has dropped the con.
            return "" # quit this handler immediately and return ""  
    # con.close()
    return buf.decode()

# Sending list of services to client
def sendservices():
    while True:
        # Reading file for accounts details
        with open("services.json") as x:
            services_dict = json.load(x)
            # Sending file for list of services to client
            print("\nSending services over...")
            servicesbytes = str(services_dict).encode()
            connection.send(servicesbytes)
            break
        if handler(connection) == 'x':
            break
    serversocket.close()

# Sending logged in user's subscription file to client
def sendsubs():
    while True:
        #Reading file for user's subscriptions
        with open("loggedinuser.json") as u:
            loggedinuser = json.load(u)
        with open(f'{loggedinuser}.txt','r') as y:
            userfile = y.read()
            # Sending file for user subs to client
            print("\nSending subscription file over...")
            userfilebytes = userfile.encode()
            connection.send(userfilebytes)
            break
        if handler(connection) == 'x':
            break
    serversocket.close()
 
def handler(con):
    while True:
        buf = con.recv(255) # buf is of the type of byte
        if len(buf) > 0:
            # print(buf.decode()) # decode with system default encoding scheme
            if buf == b"q" or buf == b"X":
                print("\nServer shut down.")
                exit(0)
            elif buf == b'usersubs':
                sendsubs()
            elif buf == b'change':
                recvlogin(connection)
            elif buf == b'services':
                sendservices()
            elif buf ==b'loggedin':
                recvname(connection)
            elif buf == b'number':
                recvnum(connection)
            elif buf == b'subs':
                recvsubs(connection)
            else:
                con.sendall(buf) # echo back the same byte sequence to client
        else: #0 length buf implies client has dropped the con.
            return "" # quit this handler immediately and return "" 
    con.close()
    return buf.decode()

# Sending users' accounts details to client
def sendlogin():
    while True:
        # Reading file for accounts details
        with open("users.json") as y:
            userlogin = json.load(y)
            # Sending file for accounts details to client
            print("\nSending account details over...")
            userloginbytes = str(userlogin).encode()
            connection.send(userloginbytes)
        if handler(connection) == 'x':
            break
    serversocket.close()

sendlogin()