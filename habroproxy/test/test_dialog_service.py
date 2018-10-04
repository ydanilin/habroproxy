from habroproxy.model.request import Request
from habroproxy.model.response import Response
from habroproxy.model.dialog import Dialog
from habroproxy.services.dialog import DialogService


def test_get_dialog_by_host():
    service = DialogService(Dialog, Request, Response)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    service.createDialog(('localhost', 8080), raw)
    _id, dialog = service.getDialogByHost('habr.com')
    assert dialog is not None
    msg = service.getLastMessage(_id)
    assert msg.host == b'habr.com'


def test_make_established_response():
    service = DialogService(Dialog, Request, Response)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    dialogId = service.createDialog(('localhost', 8080), raw)
    established = service.makeEstablishedResponse(dialogId)
    assert established == b'HTTP/1.0 200 Connection established\r\n\r\n'


def test_prepare_pyrequest_args():
    service = DialogService(Dialog, Request, Response)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    dialogId = service.createDialog(('localhost', 8080), raw)
    raw1 = b'GET / HTTP/1.1\r\nHost: habr.com\r\nUser-Agent: python-requests/2.19.1\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
    nextReq = service.makeRequestFromRaw(raw1, dialogId)
    method, url, kwargs = service.preparePyRequestArgs(nextReq, dialogId)
    assert method == 'GET'
    assert url == 'https://habr.com:443/'
    assert kwargs['headers'] == {
        'Host': 'habr.com',
        'User-Agent': 'python-requests/2.19.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    assert kwargs['stream'] == True
