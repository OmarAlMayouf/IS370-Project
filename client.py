import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12345

def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT)) #connecting to the server
        print(f"Connected to server at {SERVER_ADDRESS}:{SERVER_PORT}")
        client_socket.close()
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()