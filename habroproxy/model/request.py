from habroproxy.read import lsep, readRequestLine, readHeaders
from habroproxy.utils import prettyDict


class Request:
    def __init__(self, **params):
        self.form = ''
        self.method = ''
        self.scheme = ''
        self.host = ''
        self.port = ''
        self.path = ''
        self.http_version = ''
        self.headers = {}
        self.body = b''
        self.__dict__.update(params)
        self.dialog = None

    @classmethod
    def createFromRaw(cls, raw):
        ls = lsep()
        header, *body = raw.split(ls + ls, maxsplit=1)
        line, *tail = header.split(ls)
        lineDict = readRequestLine(line)
        headersDict = readHeaders(tail)
        return cls(**dict(lineDict, headers=headersDict, body=body[0]))

    def getFullUrl(self):
        scheme = self.scheme if self.scheme else self.dialog.scheme
        host = self.host if self.host else self.dialog.remoteHost
        port = self.port if self.port else self.dialog.remotePort
        return f'{scheme}://{host}:{port}{self.path}'

    def __str__(self):
        port = self.dialog.clientPort
        line = f'{self.method} {self.getFullUrl()} {self.http_version}'
        headers = prettyDict(self.headers)
        return f'req from {port}: {line}\nheaders: {headers}\nbody: {self.body.decode()}\n\n'
