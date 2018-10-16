""" client request entity """
from habroproxy.read import lsep, read_request_line, read_headers
from habroproxy.utils import pretty_dict


class Request:  # pylint: disable=too-many-instance-attributes
    """
        Entity to store request parameters.
        Use create_from_raw() class method to generate it.
    """
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
    def create_from_raw(cls, raw):
        """ parses http request raw text, instantiates and populates the request entity """
        ls_ = lsep()
        header, *body = raw.split(ls_ + ls_, maxsplit=1)
        line, *tail = header.split(ls_)
        line_dict = read_request_line(line)
        headers_dict = read_headers(tail)
        return cls(**dict(line_dict, headers=headers_dict, body=body[0]))

    def get_full_url(self):
        """
            "Full url" means complete string scheme://host:port/path
            When clients need https, they send relative requests after CONNECT,
            so we need to figure out scheme, host, port elsevere.
            That is where dialog entity helps
        """
        scheme = self.scheme if self.scheme else self.dialog.scheme
        host = self.host if self.host else self.dialog.remote_host
        port = self.port if self.port else self.dialog.remote_port
        return f'{scheme}://{host}:{port}{self.path}'

    def __str__(self):
        port = self.dialog.client_port
        line = f'{self.method} {self.get_full_url()} {self.http_version}'
        # headers = pretty_dict(self.headers)
        # return f'req from {port}: {line}\nheaders: {headers}\nbody: {self.body.decode()}\n\n'
        return f'req from {port}: {line}\nbody: {self.body.decode()}\n'
