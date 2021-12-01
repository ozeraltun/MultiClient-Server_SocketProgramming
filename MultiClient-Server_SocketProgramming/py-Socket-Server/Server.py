import socket
from _thread import *
from SS_Client import SSClient


class ServerNetwork:
    def __init__(self, host, port):
        self.clientList = []
        self.host = host
        self.port = port
        self.socket = self.initialize()
        start_new_thread(self.check_for_new_clients, ())
        start_new_thread(self.check_client_messages, ())
        self.printLock = False

    def initialize(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        return s

    def check_for_new_clients(self):
        while True:
            conn, address = self.socket.accept()
            while True:
                if not self.printLock:
                    self.printLock = True
                    print('\nConnected by', address)
                    self.printLock = False
                    break
            new_ss_client = SSClient(conn, address)
            self.clientList.append(new_ss_client)  # Every client has its own thread for reading value

    def check_client_messages(self):
        while True:
            for i in range(len(self.clientList)):
                if self.clientList[i].has_message(1):
                    while True:
                        if not self.printLock:
                            self.printLock = True
                            print("\nClient at index : {}, has the following message(You need to process it): {}".format(i,
                                                                        self.clientList[i].get_message(0, 1).get_message()))
                            self.printLock = False
                            break
                    self.clientList[i].remove_message(0, 1)
