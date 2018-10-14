""" Request object methods """
from habroproxy.model.request import Request


def test_create_connect():
    """ parse CONNECT request """
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    req = Request.create_from_raw(raw)
    assert req.form == 'authority'
    assert req.method == 'CONNECT'
    assert req.scheme == ''
    assert req.host == 'habr.com'
    assert req.port == '443'
    assert req.path == ''
    assert req.http_version == 'HTTP/1.0'
    assert req.headers == {}
    assert req.body == b''


def test_create_relative():
    """ parse relative request """
    # pylint: disable=line-too-long
    raw = b'GET / HTTP/1.1\r\nHost: habr.com\r\nUser-Agent: python-requests/2.19.1\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
    req = Request.create_from_raw(raw)
    assert req.form == 'relative'
    assert req.method == 'GET'
    assert req.scheme == ''
    assert req.host == ''
    assert req.port == ''
    assert req.path == '/'
    assert req.http_version == 'HTTP/1.1'
    assert req.headers == {
        'Host': 'habr.com',
        'User-Agent': 'python-requests/2.19.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    assert req.body == b''


def test_create_absolute():
    """ parse absolute request """
    # pylint: disable=line-too-long
    raw = b'GET http://www.rgbagira.ru/ HTTP/1.1\r\nHost: www.rgbagira.ru\r\nUser-Agent: python-requests/2.19.1\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
    req = Request.create_from_raw(raw)
    assert req.form == 'absolute'
    assert req.method == 'GET'
    assert req.scheme == 'http'
    assert req.host == 'www.rgbagira.ru'
    assert req.port == '80'
    assert req.path == '/'
    assert req.http_version == 'HTTP/1.1'
    assert req.headers == {
        'Host': 'www.rgbagira.ru',
        'User-Agent': 'python-requests/2.19.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    assert req.body == b''
