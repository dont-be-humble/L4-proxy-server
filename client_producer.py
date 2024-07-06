import time
import random
import threading
from client.client import Client, log_message

def handle_client(client):
    while True:
        client.ping_server()
        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    log_message("=============================================New testing started========================================")
    clients_info = [('127.0.0.1', 12345, "0.0.0.0", 8001),
                    ('127.0.0.1', 12345, "0.0.0.0", 8002),
                    ('127.0.0.1', 12345, "0.0.0.0", 8003),
                    ('127.0.0.1', 12345, "0.0.0.0", 8004),
                    ('127.0.0.1', 12345, "0.0.0.0", 8005)]
    
    clients = [Client(server_ip, server_port, client_ip, client_port) for server_ip, server_port, client_ip, client_port in clients_info]

    # set up connection
    for client in clients:
        client.set_connection()

    threads = []
    for client in clients:
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()