import socket
import threading

ALOGIN_CMD = "ALOGIN : cxpzeRGSPJEd"

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.admins = []  # list to store all connected admins
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def start(self):
        self.server.listen()
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client, address = self.server.accept()
            self.clients.append(client)
            print(f"New client connected from {address}")
            threading.Thread(target=self.handle_client, args=(client, )).start()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode()
                if message:
                    if message == ALOGIN_CMD:
                        self.admins.append(client)  # add admin to the admins list
                        print(f"♥ Админ {client.getsockname()} в чате нахуй ♥")
                    else:
                        print(f"Received message: {message}")
                        # Send message to all clients if sender is an admin
                        if client in self.admins:
                            for c in self.clients:
                                if c != client:
                                    c.sendall(message.encode())
                        else:
                            client.send("Message Received Successfully!".encode())
                else:
                    self.remove(client)
                    break
            except:
                self.remove(client)
                break

    def remove(self, client):
        if client in self.clients:
            self.clients.remove(client)
            if client in self.admins:
                print(f"♥ Админ нас покинул сука(( ♥")
                self.admins.remove(client)  # remove admin from the admins list
            else:
                print(f"Client Disconnected!")
            client.close()

if __name__ == "__main__":
    server = Server("127.0.0.1", 4202)
    server.start()