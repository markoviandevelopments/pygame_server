import socket

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and port
host = '0.0.0.0'
port = 12347
server_socket.bind((host, port))

print(f"UDP server listening on {host}:{port}")

# Receive data
while True:
    data, addr = server_socket.recvfrom(1024)  # Buffer size of 1024 bytes
    received_string = data.decode('utf-8')  # Decode bytes to string
    print(f"Received from {addr}: {received_string}")

# Close socket
server_socket.close()