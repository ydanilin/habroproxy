from habroproxy.model.request import Request
from habroproxy.model.dialog import Dialog
from habroproxy.services.dialog import DialogService


def test_get_dialog_by_host():
    service = DialogService(Dialog, Request)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    service.createDialog(('localhost', 8080), raw)
    _id, dialog = service.getDialogByHost('habr.com')
    assert dialog is not None
    msg = service.getLastMessage(_id)
    assert msg.host == b'habr.com'


def test_make_established_response():
    service = DialogService(Dialog, Request)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    dialogId = service.createDialog(('localhost', 8080), raw)
    established = service.makeEstablishedResponse(dialogId)
    assert established == b'HTTP/1.0 200 Connection established\r\n\r\n'
