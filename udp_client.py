import socket

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address
host = '172.20.10.2'
port = 12347
server_address = (host, port)

# String to send
message = "Hello, UDP Server!"

# Send the string (encode to bytes)
client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Sent to {server_address}: {message}")

# Close socket
client_socket.close()