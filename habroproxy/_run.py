"""
    Habroproxy bootstrap procedure
"""
from .model.dialog import Dialog
from .model.request import Request
from .model.response import Response
from .model.rules import TMInterceptor
from .services.dialog import DialogService
from .services.tls import TlsService
from .proxy import Server


def run():
    """
        Habroproxy bootstrap procedure. Creates all service dependencies and inject them
    """
    tm_interceptor = TMInterceptor('habr.com')
    dialog_service = DialogService(Dialog, Request, Response, [tm_interceptor])
    tls_service = TlsService()
    server = Server(('', 8080), dialog_service, tls_service)
    server.start()
    server.serve_forever()
