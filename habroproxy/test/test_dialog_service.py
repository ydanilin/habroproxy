""" Dialog service tests """
from habroproxy.model.request import Request
from habroproxy.model.response import Response
from habroproxy.model.dialog import Dialog
from habroproxy.services.dialog import DialogService


def test_get_dialog_by_host():
    """ Every dialog keeps hostname """
    service = DialogService(Dialog, Request, Response)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    service.create_dialog(('localhost', 8080), raw)
    _id, dialog = service.get_dialog_by_host('habr.com')
    assert dialog is not None
    msg = service.get_last_message(_id)
    assert msg.host == 'habr.com'


def test_make_established_response():
    """ message for clients wanted https connection """
    service = DialogService(Dialog, Request, Response)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    dialog_id = service.create_dialog(('localhost', 8080), raw)
    established = service.make_established_response(dialog_id)
    assert established == b'HTTP/1.0 200 Connection established\r\n\r\n'


def test_prepare_pyrequest_args():
    """ for python requests library """
    service = DialogService(Dialog, Request, Response)
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    dialog_id = service.create_dialog(('localhost', 8080), raw)
    # pylint: disable=line-too-long
    raw1 = b'GET / HTTP/1.1\r\nHost: habr.com\r\nUser-Agent: python-requests/2.19.1\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
    next_req = service.make_request_from_raw(raw1, dialog_id)
    method, url, kwargs = service.prepare_py_request_args(next_req)
    assert method == 'GET'
    assert url == 'https://habr.com:443/'
    assert kwargs['headers'] == {
        'Host': 'habr.com',
        'User-Agent': 'python-requests/2.19.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    assert kwargs['stream'] is True
