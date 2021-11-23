import json
import socket
import datetime
import time

print("\n============================================")
print("Welcome to Electronic Services & Protection:")
print("============================================\n")

# Codes for client socket
def getnewsocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket = getnewsocket()
host = "localhost"
clientsocket.connect((host,8089))

# List to display options 1 to 5
display_options = ["Display Our List of Services", "Search for service", "Display added services", "Payment", "Edit menu", "Display current subscriptions", "Exit ESP"]

# List for items that user adds to cart
user_cart = []

# List for number of times item added
repeat = [0,0,0,0]

# List for user to modify the cart
modify = ["Add service(s)", "Remove service(s)"]

# List of users that qualifies for discount
users = ["Amy", "Bob", "Charlie", "David","Ethan"]

# Function to print any lists with numbers
def display_lists(lists):
    global count
    count = 1
    for i in lists:
        print(f"{count}. {i}")
        count = count + 1

# Function to display services
def display1():
    # Send message 'services'
    serv = "services"
    servbytes = serv.encode()
    clientsocket.send(servbytes)
    while True:
        print("\nReceiving list of services...")
        sbuf = clientsocket.recv(255)
        if len (sbuf) > 0:
            sbuf = sbuf.decode()
            # To change ' to " for json to work
            json_acceptable_string = sbuf.replace("'", "\"")
            global services_dict
            services_dict = json.loads(json_acceptable_string)
            # List to display services
            global services
            services = list(services_dict.keys())
            break
        else:
            print("\nEnding connection with server...")
            break
    print("List of services received") 
    print("\nWe have the following service(s):")
    for i in range(len(services)):
        print(f"{i+1}. {services[i].ljust(20)}: ${services_dict[services[i]]}k/year")
    cart(services)

# Function for admin to edit the menu
def admin():
    admin_action = ""
    # Loop for admin to choose action 1 to 3
    while admin_action != "1" or "2" or "3":
        admin_action = input("\nInput 1 to add services and 2 to remove services or 3 to exit: ").strip()
        try:
            # For admin to add service to menu
            if admin_action == "1":
                # Add name of service
                newservice = input("\nPlease enter new service to be added to menu: ").strip()
                while True:
                    try:
                        # Add price of service
                        newprice = float(input("\nPlease enter price of new service (with decimal): ").strip())
                        break
                    except ValueError:
                        print("Please enter a number")

                adding_confirmation = ""
                while adding_confirmation != "Y" or "N":
                    # For admin to confirm addition of service to menu
                    adding_confirmation = input(f"\nAre you sure you want to add {newservice}, priced at ${round(newprice,1)}k/year? Y/N? ").upper().strip()
                
                    if adding_confirmation == "Y":
                        # Update dictionary in json file
                        services_dict[newservice] = newprice
                        with open("CA1 Assignment\\services.json","w") as x:
                            json.dump(services_dict,x,indent=3)
                        
                        print(f"\n{newservice} has been added.")
                        break
                    
                    elif adding_confirmation == "N":
                        print("Services will remain as before.")
                        break

            # For admin to remove service from menu
            elif admin_action == "2":
                print("")
                for i in range(len(services)):
                    print(f"{i+1}. {services[i].ljust(20)}: ${services_dict[services[i]]}k/year")

                remove = input("\nPlease enter services that you would like to remove from the menu: ").strip()

                for i in services_dict:
                    if remove.lower() in i.lower() and remove != "":
                        removal_confirmation = ""
                        while removal_confirmation != "Y" or "N":
                            # For admin to confirm the removal of service
                            removal_confirmation = input(f"Are you sure you want to remove {remove}? Y/N? ").upper().strip()
                            if removal_confirmation == "Y":
                                # Update dictionary in json file
                                del(services_dict[i])
                                with open("CA1 Assignment\\services.json","w") as x:
                                    json.dump(services_dict,x,indent=3)
                                print(f"{remove} has been removed.")
                                break

                            elif removal_confirmation == "N":
                                print("Services will remain as before")
                                break
                        break
                    
            # For admin to exit editing mode and back to menu
            elif admin_action == "3":
                print("\nExiting editing mode...\n")
                print("Returning to menu...\n")
                menu()

            else:
                print("Please input 1, 2 or 3 only")
        except ValueError:
                print("Please input 1, 2 or 3 only")
            
# Function for user to search for services
def search():
    search = ""
    while search == "":
        search = input("\nPlease input service to search: ").upper().strip()

        availlist = []
        # Loop to see if search is in the services
        for i in services:
            if search.upper() in i.upper(): 
                availlist.append(i)
            # Joins the items into a string
            avail = '\n'.join(map(str,availlist))
        if avail == "":
            print(f"Sorry, we don't have any of the service {search}!\n\nPlease choose from {services}")
            search = ""
        else:
            print("Yes, we have the following service(s):")
            for i, service in enumerate(availlist):
                print(f"{i+1}. {service.ljust(20)}: ${services_dict[service]}k/year")
            cart(availlist)

# Function for payment
def payment():
    print(f"\nPlease check services added:")
    global total
    total = 0
    for i in range(len(user_cart)):
        print(f"{i+1}. {user_cart[i].ljust(20)}: ${services_dict[user_cart[i]]}k/year\tx{repeat[i]}")
        total += float(services_dict[user_cart[i]] * repeat[i])

    # Checking for membership for 30% discount
    check_user_for_discount = input("\nPlease enter your name to check if you have a membership for discount: ").upper().strip()
    alpha_check = check_user_for_discount.isalpha()

    # Ensures that user only input alphabets for name
    while alpha_check == False:
        print("Please input alpha characters only")
        check_user_for_discount = input("\nPlease enter your name to check if you have a membership for discount: ").upper().strip()
        alpha_check = check_user_for_discount.isalpha()
        if alpha_check == True:
            continue
    # Loop through list of user who qualifies for discount
    time.sleep(1)
    for i in users:
        if check_user_for_discount.upper() == i.upper():
            print("You qualify for a 30% discount")
            total = total * 0.7
        else:
            print("Sorry, you are not part of our membership.")

        print(f"\nYour subscription will be a total of: ${round(total,2)}k/year.")

        # User officially purchasing subscriptions
        purchasing = ""
        while purchasing !="Y" or "N":
            purchasing = input("Enter Y to confirm card transaction or N to return to menu: ").upper()
            if purchasing == "Y":
                print("\nPayment processing...")

                time.sleep(1)

                print("\nPayment completed...")

                # Send message 'number'
                number = "number"
                numberbytes = number.encode()
                clientsocket.send(numberbytes)

                # Send repeat list to server
                repeatlist = str(repeat)
                repeatlistbytes = repeatlist.encode()
                clientsocket.send(repeatlistbytes)

                time.sleep(1)

                # Send message 'subs'
                subs = "subs"
                subsbytes = subs.encode()
                clientsocket.send(subsbytes)
                # Send user_cart list to server
                usercart = str(user_cart)
                usercartbytes = usercart.encode()
                clientsocket.send(usercartbytes)

                user_cart.clear()
                break
            elif purchasing == "N":
                print("Proceeding back to menu...")
                menu()
            else:
                print("Please input Y or N only")

        print("\nReturning to menu... ")
        menu()
    
# Function to add to cart
def cart(x):
    while True:
        try:
            # Prompt user to enter services to be added to cart
            add_to_cart = int(input(f"\nEnter the service 1-{len(x)} that you would like to add, or 0 to stop: ").strip())
        
            if add_to_cart > len(x):
                print(f'Service is not available! Please choose a service from number 1-{len(x)}')

            elif add_to_cart <= len(x) and add_to_cart > 0:
                if x[add_to_cart-1] not in user_cart:
                    user_cart.append(x[add_to_cart-1])
                    repeat[add_to_cart-1] = repeat[add_to_cart-1] + 1
                    print(f"{add_to_cart} is added")
                else:  
                    print(f"{add_to_cart} is added")
                    repeat[add_to_cart-1] = repeat[add_to_cart-1] + 1
            # User stops adding and check services added
            elif add_to_cart == 0:
                for i in (repeat):
                    if i == 0:
                        repeat.remove(i)
                added_services()
        except ValueError:
            print("Please enter a number!")

# Function for user to modify the cart
def modify_cart():
    user_modify = ""

    while user_modify != "Y" or "N":
        user_modify = input("\nAny changes to make to cart? Y/N: ").upper().strip()

        if user_modify == "Y":
            add_remove = ""
            while add_remove != 1 or 2:
                try:
                    display_lists(modify)
                    add_remove = int(input("\nPlease input 1 or 2 to proceed: ").strip())
        
                    if add_remove == 1:
                        # Add service
                        display1()

                    elif add_remove == 2:
                        while True:
                            print("")
                            for i in range(len(user_cart)):
                                print(f"{i+1}. {user_cart[i].ljust(20)}: ${services_dict[user_cart[i]]}k/year\tx{repeat[i]}")                     
                            # Remove service(s)
                            removal = int(input("\nEnter number for service to be removed from cart: ").strip())
                            if removal in range(len(user_cart)+1):
                                if removal > 0:
                                    print(f"\n1 of {user_cart[removal-1]} has been removed\n")
                                    repeat[removal-1] = repeat[removal-1] - 1
                                    if repeat[removal-1] == 0:
                                        del(user_cart[removal-1])
                                        del(repeat[removal-1])
                                    if user_cart != []:
                                        # Cart after removing
                                        for i in range(len(user_cart)):
                                            print(f"{i+1}. {user_cart[i].ljust(20)}: ${services_dict[user_cart[i]]}k/year\tx{repeat[i]}")
                                        cart_confirmation = ""
                                        while cart_confirmation != "N":
                                            # Ask user if removing more services
                                            cart_confirmation = input("\nAnything else to remove? Y/N? : ").upper().strip()
                                            if cart_confirmation == "N":
                                                modifydone = input("Input 1 to proceed to payment or 2 to return to menu: ")

                                                if modifydone == "1":
                                                    payment()
                                                elif modifydone == "2":
                                                    menu()
                                                else: 
                                                    print("Please input 1 or 2 only")
                                                        
                                            elif cart_confirmation == "Y":
                                                break
                                            else: 
                                                print("Please input Y or N only")
                                    else:
                                        print("\nNo items in cart...")
                                        print("\nReturning to menu...\n")
                                        menu()
                                else:
                                    print(f"Please input 1 to {len(user_cart)}")
                            else: 
                                print(f"Please input 1 to {len(user_cart)}")

                except ValueError:
                    print("Please input 1 or 2 only")
                                               
        elif user_modify == "N":
            no_modify = ""
            while no_modify != 1 or 2:
                no_modify = int(input("\nInput 1 to proceed to payment or 2 to view menu: ").strip())
                if no_modify == 1:
                    print(payment())
                elif no_modify == 2:
                    print(menu())
        else:
            print("Please input Y or N only")

# Function for displaying services added to cart
def added_services():
    if user_cart == []:
        print("\nNo items in cart...")
        print("\nReturning to menu...\n")
        menu()
    else:
        print(f"\nServices added:")
        for i in range(len(user_cart)):
            print(f"{i+1}. {user_cart[i].ljust(20)}: ${services_dict[user_cart[i]]}k/year\tx{repeat[i]}")

        after_cart = ""
        while after_cart != 1 or 2 or 3:
            try:
                after_cart = int(input("\nInput 1 to proceed to payment or 2 to modify cart or 3 to return to menu: ").strip())
                # Proceed to payment
                if after_cart == 1:
                    payment()
                # Modify cart
                elif after_cart == 2:
                    modify_cart()
                # Return to menu
                elif after_cart == 3:
                    menu()
                else:
                    print("Please input 1 to 3 only")
            except ValueError:
                print("Please input 1 to 3 only")

# Function to request server for current subscriptions [NOT DONE]
def current_sub():
    # Send message 'usersubs'
    usersubs = "usersubs"
    usersubbytes = usersubs.encode()
    clientsocket.send(usersubbytes)
    print("Requesting subscription file from server...")
    time.sleep(3)
    while True:
        print("\nReceiving subscription file...")
        ubuf = clientsocket.recv(10000)
        if len (ubuf) > 0:
            ubuf = ubuf.decode()
            print(ubuf)
            while True:
                ret = input("Input 1 to return to menu after viewing: ")
                if ret == "1":
                    menu()
                else:
                    print("Please enter 1 only")
                    
        else:
            print("\nEnding connection with server...")
            break

# Function for user login
def user_login():
    global username
    while True:
        while True:
            print("\nReceiving account details...")
            time.sleep(1)
            abuf = clientsocket.recv(255)
            if len (abuf) > 0:
                abuf = abuf.decode()
                # To change ' to " for json to work
                json_acceptable_string = abuf.replace("'", "\"")
                userlogin = json.loads(json_acceptable_string)
                break
            else:
                print("\nEnding connection with server...")
                break
        break
    print("Details received")

    while True:
        username = input("\nPlease enter your username (case-sensitive): ").strip()
        if username in userlogin:
            while True:
                password = input("Please enter your password (case-sensitive): ").strip()
                if password == userlogin[username]:
                    time.sleep(1)
                    print("\nLogin successful. Proceeding to menu...\n")

                    loggedin = "loggedin"
                    loggedinbytes = loggedin.encode()
                    clientsocket.send(loggedinbytes)

                    # Send name of user logged in
                    loggedinuser = username
                    loggedinuserbytes = loggedinuser.encode()
                    clientsocket.send(loggedinuserbytes)
                    menu()
                else:
                    print("\nPassword incorrect. Please try again")

        else:
            print("\nUser does not exist")
            relogin = int(input("\nInput 1 to try again or 2 to sign up: "))
            if relogin == 1: 
                print("Please try again")
            elif relogin == 2:
                # Send message 'change'
                msg = "change"
                msgbytes = msg.encode()
                clientsocket.send(msgbytes)

                print("\nProceeding to sign up...")
                newuser = input("\nPlease enter username for registration (case-sensitive): ")
                newpass = input ("Please enter password for registration (case-sensitive): ")
                # Update dictionary and send back to server
                userlogin[newuser] = newpass
                userloginbytes = str(userlogin).encode()
                clientsocket.send(userloginbytes)

                time.sleep(1)
                print("\n============================================")
                print(f"       {newuser}'s account has been created. ")
                print("============================================")
                print("\nProceeding to login...")

# Displaying menu
def menu():
    print("\n============================================")
    print("                   MENU                     ")
    print("============================================\n")

    choice = True

    if choice == True:
        print("")
        display_lists(display_options)
        choice = input("\nPlease input your choice of action (ENTER to exit): ").strip()
        
        if choice == "":
            if user_cart != []:
                exit_confirmation = input("There are items in cart. Are you sure you want to exit? Y/N").upper().strip()
                if exit_confirmation == "Y":
                    print("Thank you for using ESP.")
                    quits = "X"
                    quitsbyte = quits.encode()
                    clientsocket.send(quitsbyte)
                    exit(0)
                elif exit_confirmation == "N":
                    menu()
            elif user_cart == []:  
                print("Thank you for using ESP.")
                quits = "X"
                quitsbyte = quits.encode()
                clientsocket.send(quitsbyte)
                exit(0)
        elif choice == "1":
            display1()
        elif choice == "2":
            search()
        elif choice == "3":
            added_services()
        elif choice == "4":
            payment()
        elif choice == "5":
            password = input("Please input password to continue: ").strip()
            if password == "admin123":
                admin()
            else:
                print("\nEditing denied, only admins allowed!\n")
                choice == True
                menu()
        elif choice == "6":
            current_sub()
        elif choice == "7":
            if user_cart != []:
                exit_confirmation = input("There are items in cart. Are you sure you want to exit? Y/N").upper().strip()
                if exit_confirmation == "Y":
                    print("Thank you for using ESP.")
                    quits = "X"
                    quitsbyte = quits.encode()
                    clientsocket.send(quitsbyte)
                    exit(0)
                elif exit_confirmation == "N":
                    menu()
            elif user_cart == []:  
                print("Thank you for using ESP.")
                quits = "X"
                quitsbyte = quits.encode()
                clientsocket.send(quitsbyte)
                exit(0)
        else:
            choice == True
            print("Input invalid!\n")
            menu()

user_login()