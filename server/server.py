import socket
import time

# File name for logging
log_file = 'server_log.txt'

# Function to log messages with timestamp
def log_message(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write(f'[{timestamp}] {message}\n')


# creating a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding the socket to a specific address and port
server_address = ('127.0.0.1', 12345)
sock.bind(server_address)

sock.listen(5)

active_connections = {}
log_message('==========New session============')
log_message(f'Server started at {server_address[0]}:{server_address[1]}')

while True:
    print('Waiting for the connection')
    connection, client_address = sock.accept()

    try:
        print('Connection from : ', client_address)
        active_connections[client_address] = connection

        log_message(f'Connection from {client_address[0]}:{client_address[1]}')

        while True:
            connection.settimeout(8)
        # receiving the request
            request = connection.recv(1024).decode('utf-8')
            log_message(f'Received request from {client_address[0]}:{client_address[1]}: {request}')

        # sending the http response
            response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\nHello, world!'
            log_message(f'Response sent to {client_address[0]}:{client_address[1]}: {response}')

            connection.sendall(response.encode('utf-8'))
    except socket.timeout:
        print(f'Timeout: No request received from {client_address}. Closing connection.')
    finally:
        log_message(f'Connection closed with {client_address[0]}:{client_address[1]}')
        del active_connections[client_address]
        connection.close()