from Message import Message
from _thread import *


class SSClient:
    index = 0

    def __init__(self, conn, address):
        SSClient.index = SSClient.index+1
        self.connection = conn
        self.address = address
        self.messageListToClient = []
        self.messageListToServer = []
        start_new_thread(self.receive_thread, ())
        start_new_thread(self.send_to_client_thread, ())

    def send_to_client_thread(self):
        while True:
            if len(self.messageListToClient) != 0:
                message = self.get_message(0, 0)
                print("We are sending a msg to client: {}".format(message.val))
                self.send_to_client(message)
                self.remove_message(0, 0)

    def add_message(self, message, list_type):
        if list_type == 0:
            self.messageListToClient.append(message)
        elif list_type == 1:
            self.messageListToServer.append(message)

    def get_message(self, index, list_type):
        if list_type == 0:
            return self.messageListToClient[index]
        elif list_type == 1:
            return self.messageListToServer[index]

    def has_message(self, list_type):
        if list_type == 0:
            if len(self.messageListToClient) != 0:
                return True
            else:
                return False
        elif list_type == 1:
            if len(self.messageListToServer) != 0:
                return True
            else:
                return False

    def remove_message(self, index, list_type):
        # you can check index range
        if list_type == 0:
            del self.messageListToClient[index]
        elif list_type == 1:
            del self.messageListToServer[index]

    def receive_from_client(self):
        data = self.connection.recv(1024)
        data_str = data.decode("utf-8")
        return data_str

    def send_to_client(self, data):
        data_str = data.encode("utf-8")
        self.connection.send(data_str)

    def receive_thread(self):
        while True:
            try:
                # data received from client
                data = self.receive_from_client()
                message = Message(data)
                self.add_message(message, 1)
                # print("We have message from the client: log: {}".format(message.val))

            except Exception as e:
                print("CONNECTION CLOSED--catch error: ")
                print(e)
                self.connection.close()
                break

        print("CONNECTION CLOSED-thread_finish")
