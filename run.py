from proxy import Server
from receive import ReceiveService

if __name__ == '__main__':
    receiveService = ReceiveService()
    server = Server(('', 8080), None, receiveService)
    server.start()
    server.serveForever()
