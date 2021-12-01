from Server import ServerNetwork
HOST = '127.0.0.1'  # Standard loop-back interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def main():
    main_server = ServerNetwork(HOST, PORT)
    while True:
        pass
    # print("Server closed")


if __name__ == '__main__':
    main()

