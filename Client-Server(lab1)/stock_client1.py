import socket

# Client configuration
host = "127.0.0.1"
port = 8888

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

while True:
    # Receive and print the stock value from the server
    data = client_socket.recv(1024)
    stock_value = data.decode()
    print(f"Stock value received: {stock_value}")