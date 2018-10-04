from .model.dialog import Dialog
from .model.request import Request
from .model.response import Response
from .services.dialog import DialogService
from .services.tls import TlsService
from .proxy import Server


def run():
    dialogService = DialogService(Dialog, Request, Response)
    tlsService = TlsService()
    server = Server(('', 8080), dialogService, tlsService)
    server.start()
    server.serveForever()
