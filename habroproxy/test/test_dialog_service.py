from habroproxy.model.request import Request
from habroproxy.model.dialog import Dialog
from habroproxy.services.dialog import DialogService


def test_get_dialog_by_host():
    service = DialogService(Dialog, Request)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    service.createDialog(('localhost', 8080), raw)
    dialog = service.getDialogByHost('habr.com')
    assert dialog is not None
