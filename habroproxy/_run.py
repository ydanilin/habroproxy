from .model.dialog import Dialog
from .model.request import Request
from .model.response import Response
from .model.rules import TMInterceptor
from .services.dialog import DialogService
from .services.tls import TlsService
from .proxy import Server


def run():
    tmInterceptor = TMInterceptor('habr.com')
    dialogService = DialogService(Dialog, Request, Response, [tmInterceptor])
    tlsService = TlsService()
    server = Server(('', 8080), dialogService, tlsService)
    server.start()
    server.serveForever()
