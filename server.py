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

def update_price(file_path, item_name, new_price):

    menu = load_menu_from_file(file_path)
    
    if item_name in menu:
        menu[item_name]['price'] = new_price
        save_menu_to_file(menu, menu_file_path)
        return True
    else:
        return False

def update_quantity(file_path, item_name, new_quan):

    menu = load_menu_from_file(file_path)
    
    if item_name in menu:
        menu[item_name]['quantity'] = new_quan
        save_menu_to_file(menu, menu_file_path)
        return True
    else:
        return False

def delete_item(file_path, item_name):
    menu = load_menu_from_file(file_path)
    if item_name in menu:
        del menu[item_name]
        save_menu_to_file(menu, file_path)
        return True
    else:
        return False

def authenticate_owner(client_socket):
    client_socket.sendall(b"[*] Please enter your username: ")
    username = client_socket.recv(1024).decode().strip()
    
    client_socket.sendall(b"[*] Please enter your password: ")
    password = client_socket.recv(1024).decode().strip()
    
    if username in owner_credentials and owner_credentials[username] == password:
        return True, username
    else:
        return False, None

def handle_client(client_socket):
    print("Connection established with a client.")
    
    # Ask for login method
    client_socket.sendall(b"[#] Login as a...\n[#] 1. Owner\n[#] 2. Customer\n[*] Enter your choice: ")
    choice = client_socket.recv(1024).decode().strip()
    if choice == '1':
        authenticated, username = authenticate_owner(client_socket)
        if authenticated:
            client_socket.sendall(b"[+] Owner authenticated. You have privileges.")
            client_socket.sendall(username.encode())
            client_socket.recv(1024).decode().strip()
            client_socket.sendall(b"\n[#] 1. Add Item\n[#] 2. Update Price\n[#] 3. Update Quantity\n[#] 4. Delete Item\n[#] 5. Exit\n[*] Enter your choice: ")
            choice = client_socket.recv(1024).decode().strip()
            if choice == "1":
                client_socket.sendall(b"[*] Enter item name: ")
                name = client_socket.recv(1024).decode().strip()
                client_socket.sendall(b"[*] Enter item Price: ")
                price = float(client_socket.recv(1024).decode().strip())
                client_socket.sendall(b"[*] Enter item Quantity: ")
                quantity = int(client_socket.recv(1024).decode().strip())
                if quantity >= 0 and price >= 0:
                    new_item = {name: {"price": price, "quantity": quantity}}
                    menu = load_menu_from_file(menu_file_path)
                    menu.update(new_item)
                    save_menu_to_file(menu, menu_file_path)
                    client_socket.sendall(b"1")
                else:
                    client_socket.sendall(b"0")
                
            elif choice == "2":
                client_socket.sendall(b"[*] Enter item name: ")
                name = client_socket.recv(1024).decode().strip()
                client_socket.sendall(b"[*] Enter new item price: ")
                price = client_socket.recv(1024).decode().strip()
                
                if price.isdigit():
                    price = float(price)
                    if price >= 0:
                        if update_price(menu_file_path, name, price):
                            client_socket.sendall(b"1")  # Success
                        else:
                            client_socket.sendall(b"0")  # Failure (item not found)
                    else:
                        client_socket.sendall(b"-1")  # Failure (negative price)
                else:
                    client_socket.sendall(b"-1")  # Failure (invalid price format)
                    
            elif choice == "3":
                client_socket.sendall(b"[*] Enter item name: ")
                name = client_socket.recv(1024).decode().strip()

                client_socket.sendall(b"[*] Enter new item quantity: ")
                quantity_response = client_socket.recv(1024).decode().strip()
                if quantity_response.isdigit():
                    quantity = int(quantity_response)
                    if quantity >= 0:
                        if update_quantity(menu_file_path, name, quantity):
                            client_socket.sendall(b"1")  # Success
                        else:
                            client_socket.sendall(b"0")  # Failure (item not found)
                    else:
                        client_socket.sendall(b"-1")  # Failure (negative quantity)
                else:
                    client_socket.sendall(b"-1")  # Failure (invalid quantity format)

            elif choice == "4":
                client_socket.sendall(b"[*] Enter item name: ")
                name = client_socket.recv(1024).decode().strip()
                if delete_item(menu_file_path, name):
                    client_socket.sendall(b"1")
                else:
                    client_socket.sendall(b"0")
            elif choice == "5":
                print("5")
            else:
                client_socket.sendall(b"[-] Invalid input")
        else:
            client_socket.sendall(b"[-] Failed to authenticate as owner")
    elif choice == '2':
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
            handle_client(client_socket)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        soc.close()

if __name__ == "__main__":
    main()