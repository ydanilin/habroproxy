from .proxy import Server
from .receive import ReceiveService
from .send import SendService

def run():
    server = Server(('', 8080), SendService(), ReceiveService())
    server.start()
    server.serveForever()
