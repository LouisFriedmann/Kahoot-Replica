# network.py connects the client to the server
import socket
import pickle

BYTES_TO_RECEIVE = 8192*8

class Network:
    def __init__(self, server):
        self.server = server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5050
        self.addr = (self.server, self.port)
        self.data = self.connect()

    def get_data(self):
        return self.data

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(BYTES_TO_RECEIVE).decode()

        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            if isinstance(data, str):
                self.client.send(data.encode())
            else:
                self.client.send(pickle.dumps(data))

            return pickle.loads(self.client.recv(BYTES_TO_RECEIVE))

        except socket.error as e:
            print(e)