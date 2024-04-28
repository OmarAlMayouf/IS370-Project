import pickle
import socket
import os
import time

class TextColor:
    red = "\u001b[0;31m"
    green = "\u001b[0;32m"
    yellow = "\u001b[0;33m"
    end = "\u001b[0m"
    cyan = "\u001b[0;36m"
    bold = "\u001b[1m"
    magneta = "\u001b[0;35m"

t = TextColor

host = '127.0.0.1' # server address
port = 12345 # server port

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server at", host + ":" + str(port))
    return client_socket

def clear_terminal():
    dots = ['.', '..', '...','....','.....','......']
    k = 0
    for i in range(5, 0, -1):
        print(f"\r{t.red}clearing in {i} seconds{dots[k]}{t.end}", end='', flush=True)
        time.sleep(1)
        k += 1
    print("\r", end='')
    os.system('cls')

def printGUI(menu):
    separator_line = f"{t.magneta}#{t.end}" + "-" * 68 + f"{t.magneta}#{t.end}"
    print(f"{t.magneta}\n{'#' * 70}\n{t.end}{t.magneta}#{t.end}\tItem\t\t\t\t\tPrice\t\t     {t.magneta}#{t.end}\n{separator_line}")
    conuter = 1
    for item, i in menu.items():
        print(f"{t.magneta}#{t.end}\t{str(conuter).rjust(2, ' ')}.{item.ljust(38, ' ')}{str(i['price']).ljust(20, ' ')}{t.magneta}#{t.end}")
        conuter+=1
    print(f"{t.magneta}{'#' * 70}\n{t.end}")

def handle_owner_authentication(client_socket):
    response = client_socket.recv(1024).decode().strip() # enter username
    print(t.yellow,response,t.end,sep="")
    username = input("    -> ").strip()
    client_socket.sendall(username.encode())
     
    response = client_socket.recv(1024).decode().strip() # enter password
    print(t.yellow,response,t.end,sep="")
    password = input("    -> ").strip()
    client_socket.sendall(password.encode())
    
    response = client_socket.recv(1024).decode().strip()
    if response == "[+] Owner authenticated. You have privileges.":
        print(t.green,response,t.end,sep="")
        username = client_socket.recv(1024).decode().strip()
        print(t.green,"[+] Hello ",username,t.end,sep="")
        client_socket.sendall(b"message") # to not get the next message printed with hello idk why tho but this works
        
        options = client_socket.recv(1024).decode().strip()
        print(t.yellow,options,t.end,sep="")
        
        choice = input("    -> ")
        client_socket.sendall(choice.encode())
        response = client_socket.recv(1024).decode().strip() # add item step 1
        if response == "[-] Invalid input":
            print(t.red,response,t.end,sep="")
        elif choice == "1":
            print(t.yellow,response,t.end,sep="")
            name = input("    -> ")
            client_socket.sendall(name.encode()) # send item name
            response = client_socket.recv(1024).decode().strip()
            print(t.yellow,response,t.end,sep="")
            price = input("    -> ")
            client_socket.sendall(price.encode()) # send item price
            response = client_socket.recv(1024).decode().strip()
            if not price.isdigit():
                print(t.red,response,t.end,sep="")
            else:
                print(t.yellow,response,t.end,sep="")
                quantity = input("    -> ")
                client_socket.sendall(quantity.encode()) # send item quantity
                response = client_socket.recv(1024).decode().strip()
                if not quantity.isdigit():
                    print(f"{t.red}[-] Invalid price or quantity format{t.end}")
                else:
                    if response == "1":
                        print(f"{t.green}[+] Successfully added!{t.end}")
                    else:
                        print(f"{t.red}[-] Invalid price or quantity format{t.end}")
        elif choice == "2":
            print(t.yellow,response,t.end,sep="")
            name = input("    -> ")
            client_socket.sendall(name.encode()) # send item name
            response = client_socket.recv(1024).decode().strip()
            print(t.yellow,response,t.end,sep="")
            price = input("    -> ")
            client_socket.sendall(price.encode()) # send item price
            response = client_socket.recv(1024).decode().strip()
            if response == "1":
                print(f"{t.green}[+] Price updated for {name} to {float(price)}{t.end}")
            elif response == "0":
                print(f"{t.red}[-] Item {name} not found in the menu{t.end}")
            elif response == "-1":
                print(f"{t.red}[-] Invalid price format{t.end}")
            
        elif choice == "3":
            print(t.yellow,response,t.end,sep="")
            name = input("    -> ")
            client_socket.sendall(name.encode()) # send item name
            response = client_socket.recv(1024).decode().strip()
            print(t.yellow,response,t.end,sep="")
            quantity = input("    -> ")
            client_socket.sendall(quantity.encode()) # send item quantity
            response = client_socket.recv(1024).decode().strip()
            
            if response == "1":
                print(f"{t.green}[+] Quantity updated for {name} to {quantity}{t.end}")
            elif response == "0":
                print(f"{t.red}[-] Item {name} not found in the menu{t.end}")
            elif response == "-1":
                print(f"{t.red}[-] Invalid quantity format{t.end}")
            else:
                print(t.red,response,t.end,sep="")
        elif choice == "4":
            print(t.yellow,response,t.end,sep="")
            name = input("    -> ")
            client_socket.sendall(name.encode()) # send item name
            response = client_socket.recv(1024).decode().strip()
            
            if response == "1":
                print(f"{t.green}[+] Item {name} has been deleted successfully{t.end}")
            elif response == "0":
                print(f"{t.red}[-] Item {name} not found in the menu{t.end}")
            else:
                print(t.red,response,t.end,sep="")
        elif choice == "5":
            print(f"{t.cyan}{t.bold}GoodBye !{t.end}",sep="")
    else:
        print(t.red,response,t.end,sep="") # fail to authenticate

def receive_menu(client_socket):
    menu_data = client_socket.recv(1024)  # Receive menu data with appropriate buffer size
    menu = pickle.loads(menu_data)  # Deserialize menu data
    return menu

def customer_order_menu(client_socket):
    menu = receive_menu(client_socket)
    printGUI(menu)
    #client_socket.sendall(b"request prompt")
    print(t.yellow,client_socket.recv(1024).decode().strip(),t.end,sep="") # print prompt
    order = input("    -> ")
    if order == "-1":
        print(f"{t.cyan}{t.bold}GoodBye !{t.end}",sep="")
        client_socket.sendall(order.encode())
    elif not order.isdigit():
        print(f"{t.red}[-] Invalid input format{t.end}")
    else:
        client_socket.sendall(order.encode())
        response = client_socket.recv(1024).decode().strip()
        if response[1] != "-":
            print(t.yellow,response,t.end,sep="") # enter quantity
            quantity = input("    -> ")
            client_socket.sendall(quantity.encode()) # send quantity
            response = client_socket.recv(1024).decode().strip() # get response back
            if len(response) > 3 and response[1] == "-":
                print(t.red,response,t.end,sep="")
            else:
                print(t.yellow,response,t.end,sep="")
                choice = input("    -> ")
                client_socket.sendall(choice.encode()) # send choice
                if choice != "1" and choice != "2":
                    response = client_socket.recv(1024).decode().strip() # get response back
                    print(t.red,response,t.end,sep="")
                elif choice == "1":
                    error = "0"
                    while True:
                        response = client_socket.recv(1024).decode().strip()
                        print(f"{t.yellow}{response}{t.end}") # print it
                        order = input("    -> ") # enter order prompt
                        client_socket.sendall(order.encode())
                        response = client_socket.recv(1024).decode().strip()
                        if response[1] == "-":
                            error = "1"
                            print(f"{t.red}{response}{t.end}")
                            break
                        else:
                            print(f"{t.yellow}{response}{t.end}") # print it
                            quantity = input("    -> ")
                            client_socket.sendall(quantity.encode())
                            response = client_socket.recv(1024).decode().strip()
                            if quantity.isdigit():
                                if response[1] == "-":
                                    error = "1"
                                    print(f"{t.red}{response}{t.end}")
                                    break
                                else:
                                    print(f"{t.yellow}{response}{t.end}")
                                    choice = input("    -> ")
                                    client_socket.sendall(choice.encode())
                                    if not choice.isdigit():
                                        error = "1"
                                        response = client_socket.recv(1024).decode().strip()
                                        print(f"{t.red}{response}{t.end}")
                                        break
                                    elif choice != "2" and choice != "1":
                                        error = "1"
                                        response = client_socket.recv(1024).decode().strip()
                                        print(f"{t.red}{response}{t.end}")
                                        break
                                    elif choice == "2":
                                        break
                            else:
                                error = "1"
                                print(f"{t.red}{response}{t.end}")
                                break
                    if error != "1":
                        response = client_socket.recv(1024).decode().strip() # get total price
                        print(t.yellow,response,t.end,sep="")
                        response = client_socket.recv(1024).decode().strip()
                        print(t.yellow,response,t.end,sep="") # print area
                        area = input("    -> ")
                        client_socket.sendall(area.encode())
                        response = client_socket.recv(1024).decode().strip() 
                        if area.isdigit():
                            print(t.red,response,t.end,sep="")
                        else:
                            print(t.yellow,response,t.end,sep="") # print street
                            street = input("    -> ")
                            client_socket.sendall(street.encode())
                            response = client_socket.recv(1024).decode().strip() 
                            if street.isdigit():
                                print(t.red,response,t.end,sep="")
                            else:
                                print(t.yellow,response,t.end,sep="") # print home number
                                number = input("    -> ")
                                client_socket.sendall(number.encode())
                                if not number.isdigit():
                                    response = client_socket.recv(1024).decode().strip()
                                    print(t.red,response,t.end,sep="") # payment method
                                else:
                                    response = client_socket.recv(1024).decode().strip()
                                    print(t.yellow,response,t.end,sep="") # payment method
                                    choice = input("    -> ")
                                    client_socket.sendall(choice.encode())
                                    response = client_socket.recv(1024).decode().strip()
                                    if response[1] == "-":
                                        print(t.red,response,t.end,sep="") # response
                                    else:
                                        print(t.yellow,response,t.end,sep="")
                                        response = client_socket.recv(1024).decode().strip()
                                        print(t.yellow,response,t.end,sep="") # confirm order?
                                        choice = input("    -> ")
                                        client_socket.sendall(choice.encode())
                                        response = client_socket.recv(1024).decode().strip()
                                        if response[1] == "-":
                                            print(t.red,response,t.end,sep="")
                                        else:
                                            print(t.green,response,t.end,sep="")
                elif choice == "2":
                    response = client_socket.recv(1024).decode().strip() # get total price
                    print(t.yellow,response,t.end,sep="")
                    response = client_socket.recv(1024).decode().strip()
                    print(t.yellow,response,t.end,sep="") # print area
                    area = input("    -> ")
                    client_socket.sendall(area.encode())
                    response = client_socket.recv(1024).decode().strip() 
                    if area.isdigit():
                        print(t.red,response,t.end,sep="")
                    else:
                        print(t.yellow,response,t.end,sep="") # print street
                        street = input("    -> ")
                        client_socket.sendall(street.encode())
                        response = client_socket.recv(1024).decode().strip() 
                        if street.isdigit():
                            print(t.red,response,t.end,sep="")
                        else:
                            print(t.yellow,response,t.end,sep="") # print home number
                            number = input("    -> ")
                            client_socket.sendall(number.encode())
                            response = client_socket.recv(1024).decode().strip()
                            if not number.isdigit():
                                print(t.red,response,t.end,sep="") # payment method
                            else:
                                print(t.yellow,response,t.end,sep="") # payment method
                                choice = input("    -> ")
                                client_socket.sendall(choice.encode())
                                response = client_socket.recv(1024).decode().strip()
                                if response[1] == "-":
                                    print(t.red,response,t.end,sep="") # response
                                else:
                                    print(t.yellow,response,t.end,sep="")
                                    response = client_socket.recv(1024).decode().strip()
                                    print(t.yellow,response,t.end,sep="") # confirm order?
                                    choice = input("    -> ")
                                    client_socket.sendall(choice.encode())
                                    response = client_socket.recv(1024).decode().strip()
                                    if response[1] == "-":
                                        print(t.red,response,t.end,sep="")
                                    else:
                                        print(t.green,response,t.end,sep="")
        else:
            print(t.red,response,t.end,sep="")
    
def main():
    try:
        while True:
            client_socket = connect_to_server()
            print(f"{t.cyan}{t.bold}\nWelcome to the Food Delivery Network!{t.end}")
            
            # Receive login method options from server
            print(t.yellow,client_socket.recv(1024).decode().strip(),t.end,sep="")
            
            # Choose login method
            choice = input("    -> ").strip()
            client_socket.sendall(choice.encode())
            
            if choice == '1':
                handle_owner_authentication(client_socket)
                clear_terminal()
            elif choice == '2':
                customer_order_menu(client_socket)
                clear_terminal()
            elif choice =='3':
                response = client_socket.recv(1024).decode().strip()
                print(f"{t.cyan}{t.bold}{response}{t.end}")
                break
            else:
                response = client_socket.recv(1024).decode().strip()
                print(f"{t.red}{response}{t.end}")
                clear_terminal()

            client_socket.close()
    
    except Exception as e:
        print(f"{t.red}Something is wrong!{t.end} {str(e)}")

    
if __name__ == "__main__":
    main()