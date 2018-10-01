import os
import socket
import select
import threading


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
        print(f"Habroproxy server is listening to '{self.address[0]}': {self.address[1]}")

    def serveForever(self, pollInterval=0.1):
        try:
            while True:
                r, _, _ = select.select([self.socket], [], [], pollInterval)
                if self.socket in r:
                    clientSocket, clientAddress = self.socket.accept()
                    t = threading.Thread(target = self.handleConnection, args = (clientSocket, clientAddress) )
                    t.run()
        except KeyboardInterrupt:
            if self.socket:
                self.closeSocket(self.socket)

    def handleConnection(self, clientSocket, clientAddress):
        # dialog = createDialog(clientAddess)
        print(f'connection from {clientAddress}')
        # receive from client into request object
        # import pdb; pdb.set_trace()
        requestDetails = self.receiveService.receive(clientSocket)
        if requestDetails.form == 'authority':
            targetSocket = self.sendService.convertToTls(clientSocket, requestDetails)
            requestDetails = self.receiveService.receive(targetSocket)
        else:
            targetSocket = clientSocket
        # send request object to remote and receive into response object
        # response = self.sendService.sendToRemote(requestDetails)
        
        # send response object to client
        # sent = self.sendService.sendToClient(targetSocket, response)
        # print(f'Sent {sent} bytes')
        
        # close connection
        # self.closeSocket(targetSocket)
        targetSocket.close()

    def closeSocket(self, sock):
        try:
            sock.shutdown(socket.SHUT_WR)
            if os.name == "nt":
                sock.settimeout(sock.gettimeout() or 20)
                for _ in range(1024 ** 3 // 4096):
                    if not sock.recv(4096):
                        break
            sock.shutdown(socket.SHUT_RD)
        except socket.error:
            pass
        sock.close()
