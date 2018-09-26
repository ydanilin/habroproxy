class RequestDetails:
    def __init__(self, requestLineDict, headers, body):
        self._requestLineDict = requestLineDict
        self._headers = headers
        self._body = body

    @property
    def form(self):
        return self._requestLineDict['form']

    @property
    def method(self):
        return self._requestLineDict['method'].decode('ascii')

    @property
    def scheme(self):
        return self._requestLineDict['scheme'].decode('ascii')

    @property
    def host(self):
        return self._requestLineDict['host'].decode('ascii')

    @property
    def port(self):
        return self._requestLineDict['port']

    @property
    def path(self):
        return self._requestLineDict['path'].decode('ascii')

    @property
    def http_version(self):
        return self._requestLineDict['http_version'].decode('ascii')

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body

    def getUrl(self):
        t = f'{self.scheme}://{self.host}:{self.port}{self.path}'
        return t
