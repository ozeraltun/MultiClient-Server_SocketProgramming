from Client import ClientNetwork
from Message import Message

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def main():
    ClientNetwork(HOST, PORT)

    client = ClientNetwork.getInstance()
    message1 = Message("First message from client1")
    message2 = Message("Second message from client1")

    client.add_message(message1)
    client.add_message(message2)

    while True:
        pass


if __name__ == "__main__":
    main()
