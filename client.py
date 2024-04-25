import pickle
import socket

class TextColor:
    red = "\u001b[0;31m"
    green = "\u001b[0;32m"
    yellow = "\u001b[0;33m"
    end = "\u001b[0m"
    cyan = "\u001b[0;36m"
    bold = "\u001b[1m"

t = TextColor

host = '127.0.0.1' # server address
port = 12345 # server port

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server at", host + ":" + str(port))
    return client_socket

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
            price = float(input("    -> "))
            client_socket.sendall(str(price).encode()) # send item price
            
            response = client_socket.recv(1024).decode().strip()
            print(t.yellow,response,t.end,sep="")
            quantity = int(input("    -> "))
            client_socket.sendall(str(quantity).encode()) # send item quantity
            
            response = client_socket.recv(1024).decode().strip()
            if response == "1":
                print(f"{t.green}[+] Successfully added!{t.end}")
            else:
                print(f"{t.red}[-] Invalid price or quantity format{t.end}") # added successfully
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
    for item, price in menu.items():
        print(f"{item}: {price}")

def main():
    try:
        client_socket = connect_to_server()
        print(f"{t.cyan}{t.bold}\nWelcome to the Food Delivery Network!{t.end}")
        
        # Receive login method options from server
        print(t.yellow,client_socket.recv(1024).decode().strip(),t.end,sep="")
        
        # Choose login method
        choice = input("    -> ").strip()
        client_socket.sendall(choice.encode())
        
        if choice == '1':
            handle_owner_authentication(client_socket)
        elif choice == '2':
            customer_order_menu(client_socket)
        else:
            print(f"{t.red}Invalid choice.{t.end}")

        client_socket.close()
    
    except:
        print(f"{t.red}Something is wrong!{t.end}")    

    
if __name__ == "__main__":
    main()