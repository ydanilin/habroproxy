from proxy import Server
from receive import ReceiveService
from send import SendService

if __name__ == '__main__':
    server = Server(('', 8080), SendService(), ReceiveService())
    server.start()
    server.serveForever()
