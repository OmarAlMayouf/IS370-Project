import socket

host = '127.0.0.1' # server address
port = 12345 # server port

def main():
    
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket
        soc.bind((host, port)) #mapping the address and port to the server
        soc.listen(5) #listen for connection >> queue up to 5 requests
        print(f"Server listening on {host}:{port}")
        
        while True:
            client_socket, client_address = soc.accept() #Accept connection
            print(f"Connection from {client_address}")
            #TODO Here later @Omar. for now the connection is kept on.
            client_socket.close()
               
    except Exception as e:
        print("An error occurred:", e)
        
    finally:
        soc.close()

if __name__ == "__main__":
    main()