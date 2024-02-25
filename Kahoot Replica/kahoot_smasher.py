# kahoot_smasher.py allows you to spam this kahoot with a name of your choosing

import socket
import pickle

BYTES_TO_RECEIVE = 8192*8
CHARACTER_LIMIT = 10
TIMES_LIMIT = 50

class SmasherNetwork:
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
                return self.client.recv(BYTES_TO_RECEIVE).decode()
            else:
                self.client.send(pickle.dumps(data))
                return pickle.loads(self.client.recv(BYTES_TO_RECEIVE))

        except socket.error as e:
            print(e)


class KahootSmasher:
    def __init__(self):
        self.spam_name = None
        self.times = None
        self.seconds = None

    def set(self, name, times, seconds):
        self.spam_name = name
        self.times = times
        self.seconds = seconds

if __name__ == "__main__":
    server = input("Please enter the IP4 address of the server you are connecting to: ")

    print("Get ready to spam this kahoot!")

    network = SmasherNetwork(server)
    data = network.get_data()

    # Tell the server this is the kahoot spammer
    data = network.send("spammer")
    if data == "Host has disabled spamming!!! Too bad so sad.":
        print("Host has disabled spamming!!! Too bad so sad.")

    else:
        # When spamming is enabled, prompt user for info related to spamming the kahoot
        kahoot_smasher = KahootSmasher()

        name = input(f"Enter a name ({CHARACTER_LIMIT} characters or less) that will be used to spam this kahoot: ")
        while len(name) > CHARACTER_LIMIT:
            name = input(f"Name must be less {CHARACTER_LIMIT} characters or less: ")

        times = input("How many times would you like a version of this name to be spammed? ")
        while not times.isdigit() or int(times) <= 0 and int(times) > TIMES_LIMIT:
            times = input(f"Times must be a number greater than zero and less than or equal to {TIMES_LIMIT}: ")
        times = int(times)

        seconds = input("How many seconds would you like this to happen for? ")
        while not seconds.isdigit() and int(seconds) <= 0:
            seconds = input("Seconds must be a number greater than zero: ")
        seconds = int(seconds)

        kahoot_smasher.set(name, times, seconds)
        print("Time to spam!!!")
        data = network.send(kahoot_smasher)