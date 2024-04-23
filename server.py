import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12345

def main():
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket
        server_socket.bind((SERVER_ADDRESS, SERVER_PORT)) #mapping the address and port to the server
        server_socket.listen(5) #listen for connection
        print(f"Server listening on {SERVER_ADDRESS}:{SERVER_PORT}")
        
        while True:
            client_socket, client_address = server_socket.accept() #Accept connection
            print(f"Connection from {client_address}")
            #TODO Here later @Omar. for now the connection is kept on.
            client_socket.close()
               
    except Exception as e:
        print("An error occurred:", e)
        
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()