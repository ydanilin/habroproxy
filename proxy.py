import socket

class Server:
    def __init__(self, address, sendService, receiveService):
        self.address = address
        self.sendService = sendService
        self.receiveService = receiveService
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.bind(self.address)
        self.socket.listen()

    def serveForever(self):
        try:
            while True:
                puk = 1
        except KeyboardInterrupt:
            if self.socket:
                self.socket.close()
