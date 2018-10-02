from habroproxy.model.request import Request


def test_create_connect():
    raw = b'CONNECT habr.com:443 HTTP/1.0\r\n\r\n'
    req = Request.createFromRaw(raw)
    assert req.form == 'authority'
    assert req.method == b'CONNECT'
    assert req.scheme == None
    assert req.host == b'habr.com'
    assert req.port == 443
    assert req.path == None
    assert req.http_version == b'HTTP/1.0'
    assert req.headers == {}
    assert req.body == b''


def test_create_relative():
    raw = b'GET / HTTP/1.1\r\nHost: habr.com\r\nUser-Agent: python-requests/2.19.1\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
    req = Request.createFromRaw(raw)
    assert req.form == 'relative'
    assert req.method == b'GET'
    assert req.scheme == None
    assert req.host == None
    assert req.port == None
    assert req.path == b'/'
    assert req.http_version == b'HTTP/1.1'
    assert req.headers == {
        'Host': b'habr.com',
        'User-Agent': b'python-requests/2.19.1',
        'Accept-Encoding': b'gzip, deflate',
        'Accept': b'*/*',
        'Connection': b'keep-alive',
    }
    assert req.body == b''


def test_create_absolute():
    raw = b'GET http://www.rgbagira.ru/ HTTP/1.1\r\nHost: www.rgbagira.ru\r\nUser-Agent: python-requests/2.19.1\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
    req = Request.createFromRaw(raw)
    assert req.form == 'absolute'
    assert req.method == b'GET'
    assert req.scheme == b'http'
    assert req.host == b'www.rgbagira.ru'
    assert req.port == 80
    assert req.path == b'/'
    assert req.http_version == b'HTTP/1.1'
    assert req.headers == {
        'Host': b'www.rgbagira.ru',
        'User-Agent': b'python-requests/2.19.1',
        'Accept-Encoding': b'gzip, deflate',
        'Accept': b'*/*',
        'Connection': b'keep-alive',
    }
    assert req.body == b''
