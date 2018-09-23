class RequestDetails:
    def __init__(self,
        form,
        method,
        scheme,
        host,
        port,
        path,
        http_version,
        headers,
        body
    ):
        self._form = form
        self._method = method
        self._scheme = scheme
        self._host = host
        self._port = port
        self._path = path
        self._http_version = http_version
        self._headers = headers
        self._body = body

    @property
    def form(self):
        return self._form

    @property
    def method(self):
        return self._method.decode('ascii')

    @property
    def scheme(self):
        return self._scheme.decode('ascii')

    @property
    def host(self):
        return self._host.decode('ascii')

    @property
    def port(self):
        return self._port

    @property
    def path(self):
        return self._path.decode('ascii')

    @property
    def http_version(self):
        return self._http_version.decode('ascii')

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body

    def getUrl(self):
        t = f'{self.scheme}://{self.host}:{self.port}{self.path}'
        return t
