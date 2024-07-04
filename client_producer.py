import time
import random
import threading
from client import Client

def handle_client(client):
    while True:
        client.ping_server()
        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    clients_info = [("192.168.1.1", 8001),
                    ("192.168.1.2", 8001),
                    ("192.168.1.3", 8001),
                    ("192.168.1.4", 8001),
                    ("192.168.1.5", 8001)]
    
    clients = [Client(ip, port) for ip, port in clients_info]

    # set up connection
    for client in clients:
        client.set_connection()

    threads = []
    for client in clients:
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()