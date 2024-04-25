import pickle
import socket
import yaml

host = '127.0.0.1'  # server address
port = 12345  # server port
menu_file_path = 'menuPrices.yaml'  # path of the file
owner_credentials = {"admin": "admin"}

def load_menu_from_file(file_path):
    with open(file_path, 'r') as file:
        menu_data = yaml.safe_load(file)
    return menu_data

def save_menu_to_file(menu_data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(menu_data, file)

def authenticate_owner(client_socket):
    client_socket.sendall(b"[*] Please enter your username: ")
    username = client_socket.recv(1024).decode().strip()
    print(f"username : {username}")
    client_socket.sendall(b"[*] Please enter your password: ")
    password = client_socket.recv(1024).decode().strip()
    print(f"password : {password}")
    
    if username in owner_credentials and owner_credentials[username] == password:
        return True
    else:
        return False



def handle_client(client_socket):
    print("Connection established with a client.")
    
    # Ask for login method
    client_socket.sendall(b"[#] Login as a...\n[#] 1. Owner\n[#] 2. Customer\n[*] Enter your choice: ")
    choice = client_socket.recv(1024).decode().strip()
    if choice == '1':
        if authenticate_owner(client_socket):
            client_socket.sendall(b"[+] Owner authenticated. You have privileges.")
            print("Owner authenticated.")
        else:
            client_socket.sendall(b"[-] Failed to authenticate as owner.")
            print("Owner authentication failed.")
    elif choice == '2':
        print("Customer connected.")
        menu = load_menu_from_file(menu_file_path)
        menu = pickle.dumps(menu)  # Serialize menu data
        client_socket.sendall(menu)
    else:
        print("Invalid choice.")

    client_socket.close()


def main():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating socket
        soc.bind((host, port))  # mapping the address and port to the server
        soc.listen(5)  # listen for connection >> queue up to 5 requests
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = soc.accept()  # Accept connection
            print(f"Connection from {client_address}")

            # Handle client communication in a separate thread
            handle_client(client_socket)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        soc.close()

if __name__ == "__main__":
    main()