import socket

host = '127.0.0.1' # client address
port = 12345 # client port

def main():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket
        soc.connect((host, port)) #connecting to the server
        print(f"Connected to server at {host}:{port}")
        soc.close()
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()