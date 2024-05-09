import json
import pickle
import socket
import random

host = '127.0.0.1'  # server address
port = 12345  # server port
menu_file_path = 'menu.json'  # path of the file
owner_credentials = {"admin": "admin"}

def load_menu_from_file(file_path):
    with open(file_path, 'r') as file:
        menu = json.load(file)
    return menu

def save_menu_to_file(menu, file_path):
    with open(file_path, 'w') as file:
        json.dump(menu, file, indent=4)

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
    
def get_itemname(order):
    list = {}
    counter = 1
    menu = load_menu_from_file(menu_file_path)
    for i in menu:
        new_item = {str(counter): i}
        list.update(new_item)
        counter +=1
    for number in list:
        if number == order:
            return list[number]
    return -1

def get_quantity(name):
    menu = load_menu_from_file(menu_file_path)
    for i in menu:
        if i == name:
            return menu[i]['quantity']
    return 0

def handle_client(client_socket):
    print("Connection established with a client.")
    
    # Ask for login method
    client_socket.sendall(b"[#] Login as a...\n[#] 1. Owner\n[#] 2. Customer\n[#] 3. Exit\n[*] Enter your choice: ")
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
                price = client_socket.recv(1024).decode().strip()
                if not price.isdigit():
                    client_socket.sendall(b"[-] Invalid Price format: ")
                else:
                    price = float(price)
                    client_socket.sendall(b"[*] Enter item Quantity: ")
                    quantity = client_socket.recv(1024).decode().strip()
                    if not quantity.isdigit():
                        client_socket.sendall(b"[-] Invalid quantity format: ")
                    else:
                        quantity = int(quantity)
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
        order_list = {}
        
        client_socket.sendall(b"[*] What would you like to order? (-1 to exit)")
        order = client_socket.recv(1024).decode().strip()
        if order != "-1":
            item_name = get_itemname(order)
            if item_name != -1:
                max = get_quantity(item_name)
                syntax = f"[*] Please enter a quantity (Max. {max})"
                client_socket.sendall(syntax.encode())
                quantity = client_socket.recv(1024).decode().strip()
                if quantity.isdigit():
                    if int(quantity) < 1 or int(quantity) > int(max):
                        client_socket.sendall(b"[-] Invalid amount")
                    else:
                        new = {item_name : quantity}
                        order_list.update(new)
                        client_socket.sendall(b"[*] Would you like to add anything else? (1.yes / 2.no)")
                        choice = client_socket.recv(1024).decode().strip()
                        if choice.isdigit():
                            if int(choice) == 2:
                                menu = load_menu_from_file(menu_file_path)
                                total_price = int(quantity) * float(menu[item_name]['price'])
                                string_total_price = f"[#] Total price for {quantity} {item_name}(s) is {float(total_price)} SR"
                                client_socket.sendall(string_total_price.encode())
                                client_socket.sendall("[#] Please fill your address\n[*] Enter your area: ".encode())
                                area = client_socket.recv(1024).decode().strip()
                                if area.isdigit():
                                    client_socket.sendall(b"[-] Invalid input format {area cannot be digit}")
                                else:
                                    client_socket.sendall("[*] Enter your street: ".encode())
                                    street = client_socket.recv(1024).decode().strip()
                                    if street.isdigit():
                                        client_socket.sendall(b"[-] Invalid input format {street cannot be digit}")
                                    else:
                                        client_socket.sendall("[*] Enter your home/apt number: ".encode())
                                        number = client_socket.recv(1024).decode().strip()
                                        if not number.isdigit():
                                            client_socket.sendall(b"[-] Invalid input format {home/apt number must be digit}")
                                        else:
                                            payment = "[#] Please Enter a payment method\n[#] 1.Cash On Delivery\n[#] 2.CreditCard(Unavailable right now)\n[*] Enter your choice: "
                                            client_socket.sendall(payment.encode())
                                            choice = client_socket.recv(1024).decode().strip()
                                            if choice != "1":
                                                client_socket.sendall(b"[-] Invalid input format")
                                            else:
                                                address = f"\n\tArea: {area}\n\tStreet: {street}\n\tHome/Apt: {number}"
                                                summary = f"[#] Your order summary\n[#] Order: {quantity} {item_name}(s)\n[#] total price: {total_price} SR\n[#] Address: {address}"
                                                client_socket.sendall(summary.encode())
                                                client_socket.sendall(b"[*] Confirm order? (1.yes/2.no)")
                                                confirmation = client_socket.recv(1024).decode().strip()
                                                if confirmation != "1" and confirmation != "2":
                                                    client_socket.sendall(b"[-] Invalid input format")
                                                elif confirmation == "1":
                                                    number = random.randint(1000000,1500000)
                                                    number2 = random.randint(18,35)
                                                    print(f"New Order #{number}")
                                                    recipt = f"Thank You For Ordering\nYour Order number is #{number}\nEstimated time = {number2}"
                                                    client_socket.sendall(recipt.encode())
                                                    update_quantity(menu_file_path, item_name, (int(max) - int(quantity)))
                                                elif confirmation == "2":
                                                    client_socket.sendall(b"[-] Order Cancelled")
                            elif int(choice) == 1:
                                error = "0"
                                while True:
                                    client_socket.sendall(b"[*] What else would you like to order?")
                                    order = client_socket.recv(1024).decode().strip()
                                    item_name = get_itemname(order)
                                    if item_name != -1:
                                        max = get_quantity(item_name)
                                        syntax = f"[*] Please enter a quantity (Max. {max})"
                                        client_socket.sendall(syntax.encode())
                                        quantity = client_socket.recv(1024).decode().strip()
                                        if quantity.isdigit():
                                            if int(quantity) < 1 or int(quantity) > int(max):
                                                error = "1"
                                                client_socket.sendall(b"[-] Invalid amount")
                                                break
                                            else:
                                                new_item = {item_name : quantity}
                                                order_list.update(new_item)
                                                client_socket.sendall(b"[*] Would you like to add anything else? (1.yes / 2.no)")
                                                choice = client_socket.recv(1024).decode().strip()      
                                                if not choice.isdigit():
                                                    error = "1"
                                                    client_socket.sendall(b"[-] Invalid input format")
                                                    break
                                                elif choice != "2" and choice != "1":
                                                    error = "1"
                                                    client_socket.sendall(b"[-] Invalid input format")
                                                    break
                                                if choice == "2":
                                                    break
                                        else:
                                            error = "1"
                                            client_socket.sendall(b"[-] Invalid quantity format")
                                            break
                                    else:
                                        error = "1"
                                        client_socket.sendall(b"[-] No such order with this number")
                                        break
                                if error != "1":
                                    menu = load_menu_from_file(menu_file_path)
                                    total_price = 0.0
                                    for i,k in order_list.items():
                                        total_price += int(k) * float(menu[i]['price'])
                                    string_total_price = f"[#] Total price for your order is {float(total_price)} SR"
                                    client_socket.sendall(string_total_price.encode())
                                    client_socket.sendall("[#] Please fill your address\n[*] Enter your area: ".encode())
                                    area = client_socket.recv(1024).decode().strip()
                                    if area.isdigit():
                                        client_socket.sendall(b"[-] Invalid input format {area cannot be digit}")
                                    else:
                                        client_socket.sendall("[*] Enter your street: ".encode())
                                        street = client_socket.recv(1024).decode().strip()
                                        if street.isdigit():
                                            client_socket.sendall(b"[-] Invalid input format {street cannot be digit}")
                                        else:
                                            client_socket.sendall("[*] Enter your home/apt number: ".encode())
                                            number = client_socket.recv(1024).decode().strip()
                                            if not number.isdigit():
                                                client_socket.sendall(b"[-] Invalid input format {home/apt number must be digit}")
                                            else:
                                                payment = "[#] Please Enter a payment method\n[#] 1.Cash On Delivery\n[#] 2.CreditCard(Unavailable right now)\n[*] Enter your choice: "
                                                client_socket.sendall(payment.encode())
                                                choice = client_socket.recv(1024).decode().strip()
                                                if choice != "1":
                                                    client_socket.sendall(b"[-] Invalid input format")
                                                else:
                                                    address = f"\n\tArea: {area}\n\tStreet: {street}\n\tHome/Apt: {number}"
                                                    syntax = "Order: "
                                                    result = ""
                                                    for i, k in order_list.items():
                                                        new = f"{k} {i}(s), "
                                                        result += new
                                                    summary = f"[#] Your order summary\n[#] {syntax}{result}\n[#] total price: {total_price} SR\n[#] Address: {address}"
                                                    client_socket.sendall(summary.encode())
                                                    client_socket.sendall(b"[*] Confirm order? (1.yes/2.no)")
                                                    confirmation = client_socket.recv(1024).decode().strip()
                                                    if confirmation != "1" and confirmation != "2":
                                                        client_socket.sendall(b"[-] Invalid input format")
                                                    elif confirmation == "1":
                                                        number = random.randint(1000000,1500000)
                                                        number2 = random.randint(18,35)
                                                        print(f"New Order #{number}")
                                                        recipt = f"Thank You For Ordering\nYour Order number is #{number}\nEstimated time = {number2}"
                                                        client_socket.sendall(recipt.encode())
                                                        for i, k in order_list.items():
                                                            max = int(get_quantity(i))
                                                            new = max - int(k)
                                                            update_quantity(menu_file_path, i, new)
                                                    elif confirmation == "2":
                                                        client_socket.sendall(b"[-] Order Cancelled")
                                else:
                                    print("error")
                            else:
                                client_socket.sendall(b"[-] Invalid input format Please choose 1 or 2")
                        else:
                            client_socket.sendall(b"[-] Invalid input format")
                else:
                    client_socket.sendall(b"[-] Invalid input format")
            else:
                client_socket.sendall(b"[-] No such order with this number")
        else:
            print("-1")
    elif choice == '3':
        client_socket.sendall(b"Goodbye !")
    else:
        client_socket.sendall(b"[-] Invalid choice")
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