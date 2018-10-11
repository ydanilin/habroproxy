from habroproxy.utils import prettyDict


class Response:
    def __init__(self, **params):
        self.version = ''
        self.statusCode = 0
        self.reason = ''
        self.headers = {}
        self.cookies = None
        self.body = b''
        self.__dict__.update(params)
        self.dialog = None

    @classmethod
    def createFromPyResponse(cls, response):
        version = 'HTTP/1.1' if response.raw.version == 11 else 'HTTP/1.0'
        statusCode = response.status_code
        reason = response.reason
        # hdDict = response.headers._store.items()
        headers = response.headers
        cookies = response.cookies
        body = response.raw.read()
        return cls(**dict(
            version=version,
            statusCode=statusCode,
            reason=reason,
            headers=headers,
            cookies=cookies,
            body=body
            )
        )

    def makeRaw(self):
        firstLine = f'{self.version} {self.statusCode} {self.reason}'.encode()
        hdList = list(map(lambda x: f'{x[0]}: {x[1]}'.encode(), dict(self.headers).items()))
        headers = b'\r\n'.join(hdList)
        if self.headers.get('transfer-encoding') == 'chunked':
            passBody = b'%x\r\n%s\r\n0\r\n\r\n' % (len(self.body), self.body)
        else:
            passBody = self.body
        return b'%s\r\n%s\r\n\r\n%s' % (firstLine, headers, passBody)

    def getRemoteHost(self):
        return self.dialog.remoteHost

    def __str__(self):
        remoteHost = self.dialog.remoteHost
        port = self.dialog.clientPort
        line = f'{self.version} {self.statusCode} {self.reason}'
        headers = prettyDict(self.headers)
        return f'resp from {remoteHost} for {port}: {line}\nheaders: {headers}\ncookies: {self.cookies}\nbody length: {len(self.body)}\n\n'
