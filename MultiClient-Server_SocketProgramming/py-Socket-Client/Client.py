import socket
from _thread import *
from Message import Message
from time import sleep

class ClientNetwork:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ClientNetwork.__instance is None:
            ClientNetwork()
        return ClientNetwork.__instance

    def __init__(self, host, port):
        if ClientNetwork.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ClientNetwork.__instance = self
            self.host = host
            self.port = port
            self.message_list_to_network = []
            self.message_list_to_client = []
            # self.processed_messages = []

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
            start_new_thread(self.read_server_messages_thread, ())
            start_new_thread(self.read_client_messages_thread, ())

    def add_message(self, message):
        self.message_list_to_network.append(message)

    def send_to_server(self, message):
        self.s.sendall(message.get_message().encode("utf-8"))

    def receive_from_server(self):
        data = self.s.recv(1024)
        str_data = data.decode("utf-8")
        return str_data

    def read_server_messages_thread(self):
        while True:
            try:
                data = self.receive_from_server()
                print("data received: {}".format(data))
                message = Message(data)
                print("message is {}".format(message.get_message()))

                self.message_list_to_client.append(message)
                print("message has created")

            except Exception as e:
                print("CONNECTION CLOSED-error: ")
                print(e)
                self.s.close()
                break

        print("CONNECTION CLOSED-thread_finish")

    def read_client_messages_thread(self):
        while True:
            if len(self.message_list_to_network) != 0:  # then there is a message that must be send:
                message = self.message_list_to_network[0]
                self.send_to_server(message)
                sleep(1)
                del self.message_list_to_network[0]
