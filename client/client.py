import socket
import time
import threading

log_file = 'client/client_log.txt'
log_lock = threading.Lock()

def log_message(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Get timestamp with milliseconds
    with log_lock:
        with open(log_file, 'a') as f:
            f.write(f'[{timestamp}] {message}\n')

class Client:
    def __init__(self, server_ip, server_port, client_ip, client_port):
        self.server_ip = server_ip
        self.client_ip = client_ip
        self.server_port = server_port
        self.client_port = client_port
        self.server_address = (server_ip, server_port)
        self.client_address = (client_ip, client_port)
        self.connection = None

    def set_connection(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind(self.client_address)
        self.connection.connect(self.server_address)
        print(f'Connected to server at {self.server_address} from client at {self.client_address}')
        log_message(f'Connected to server at {self.server_address} from client at {self.client_address}')

    def ping_server(self):
        try:
            # Send a request to the server
            request = 'GET / HTTP/1.1\r\nHost: {}\r\n\r\nHi'.format(self.server_address[0])
            self.connection.sendall(request.encode('utf-8'))
            print(f'Sent request to {self.server_address}')
            log_message(f'Sent request from {self.client_port} to {self.server_address}: \n{request}')

            # Receive the response from the server
            response = self.connection.recv(1024).decode('utf-8')
            print(f'Received response from {self.server_address}: {response}')
            log_message(f'Received response from {self.server_address} to {self.client_port}: \n{response}')
        
        except socket.error as e:
            print(f'Error: {e}')