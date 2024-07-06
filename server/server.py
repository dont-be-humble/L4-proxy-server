import socket
import threading
import time

# File name for logging
log_file = 'server_log.txt'
log_lock = threading.Lock()  # Lock to ensure thread-safe logging

# Function to log messages with timestamp including milliseconds
def log_message(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Get timestamp with milliseconds
    with log_lock:  # Acquire the lock before writing to the log file
        with open(log_file, 'a') as f:
            f.write(f'[{timestamp}] {message}\n')

# Function to handle each client connection
def handle_client(connection, client_address):
    try:
        log_message(f'Connection from {client_address[0]}:{client_address[1]}')
        
        while True:
            connection.settimeout(8)
            try:
                # Receiving the request
                request = connection.recv(1024).decode('utf-8')
                if not request:
                    raise socket.timeout  # No data received, consider as timeout
                log_message(f'Received request from {client_address[0]}:{client_address[1]}: {request}')
                
                # Sending the HTTP response
                response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\nHello, world!'
                log_message(f'Response sent to {client_address[0]}:{client_address[1]}: {response}')
                connection.sendall(response.encode('utf-8'))
            except socket.timeout:
                print(f'Timeout: No request received from {client_address}. Closing connection.')
                break
    finally:
        log_message(f'Connection closed with {client_address[0]}:{client_address[1]}')
        connection.close()

# Creating a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the socket to a specific address and port
server_address = ('127.0.0.1', 12345)
sock.bind(server_address)

sock.listen(10)
log_message('============================================New session========================================')
log_message(f'Server started at {server_address[0]}:{server_address[1]}')

while True:
    print('Waiting for the connection')
    connection, client_address = sock.accept()
    threading.Thread(target=handle_client, args=(connection, client_address)).start()
