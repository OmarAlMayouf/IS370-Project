import pickle
import socket

class TextColor:
    red = "\u001b[0;31m"
    green = "\u001b[0;32m"
    yellow = "\u001b[0;33m"
    end = "\u001b[0m"
    cyan = "\u001b[0;36m"

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
    else:
        print(t.red,response,t.end,sep="")

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
        print(f"{t.cyan}\nWelcome to the Food Delivery Network!{t.end}")
        
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