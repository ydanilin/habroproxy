from habroproxy.read import lsep, readRequestLine, readHeaders

class Request:
    def __init__(self, **params):
        self.form = ''
        self.method = b''
        self.scheme = b''
        self.host = b''
        self.port = 0
        self.path = b''
        self.http_version = b''
        self.headers = {}
        self.body = b''
        self.__dict__.update(params)

    @classmethod
    def createFromRaw(cls, raw):
        ls = lsep()
        header, *body = raw.split(ls + ls, maxsplit=1)
        line, *tail = header.split(ls)
        lineDict = readRequestLine(line)
        headersDict = readHeaders(tail)
        return cls(**dict(lineDict, headers=headersDict, body=body[0]))
