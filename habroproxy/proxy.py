import os
import socket
import select
import threading
import requests
from OpenSSL import SSL


class Server:
    def __init__(self, address, dialogService, tlsService):
        self.address = address
        self.dialogService = dialogService
        self.tlsService = tlsService
        self.socket = None
        self.pollInterval = 0.1

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
        print(f'connection from {clientAddress}')
        rawMessage = self.read(clientSocket)
        print(rawMessage)
        dialogId = self.dialogService.createDialog(clientAddress, rawMessage)
        request = self.dialogService.getLastMessage(dialogId)
        if request.form == 'authority':
            clientSocket.sendall(self.dialogService.makeEstablishedResponse(dialogId))
            context = self.tlsService.createSslContext(request.host.decode())
            secure = SSL.Connection(context, clientSocket)
            secure.set_accept_state()
            try:
                secure.do_handshake()
            except SSL.Error as v:
                print("SSL handshake error: %s" % repr(v))
                secure.close()
            targetSocket = secure
            # read application data request after handshake
            postHandshakeRaw = self.read(targetSocket)
            print(postHandshakeRaw)
            finalRequest = self.dialogService.makeRequestFromRaw(postHandshakeRaw, dialogId)
        else:
            targetSocket = clientSocket
            finalRequest = request
        # now go to remote
        method, url, kwargs = self.dialogService.preparePyRequestArgs(finalRequest, dialogId)
        # send request object to remote and receive into response object
        # pyResponse
        response = requests.request(method, url, **kwargs)
        print(response.headers)
        # send response object to client
        # sent = self.sendService.sendToClient(targetSocket, response)
        # print(f'Sent {sent} bytes')
        
        # close connection
        # self.closeSocket(targetSocket)
        targetSocket.close()

    def read(self, sock):
        rawMessage = b''
        while True:
            r, _, _ = select.select([sock], [], [], self.pollInterval)
            if sock in r:
                try:
                    chunk = sock.recv(1024)
                    rawMessage += chunk
                except socket.error:
                    break  # TODO construct exeption
            else:
                break
        return rawMessage

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
