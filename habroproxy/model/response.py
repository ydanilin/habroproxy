""" remote response entity """
from habroproxy.utils import pretty_dict


class Response:
    """
        Entity to store remote response parameters.
        Use create_from_py_response() class method to generate it.
    """
    def __init__(self, **params):
        self.version = ''
        self.status_code = 0
        self.reason = ''
        self.headers = {}
        self.cookies = None
        self.body = b''
        self.__dict__.update(params)
        self.dialog = None

    @classmethod
    def create_from_py_response(cls, response):
        """
            As we use requests library to communicate with remote, this method creates
            _our_ response from corresponding requests Response class.
            The reason we do not use library's response directly is that we need
            http version string missing in library class, along with raw body.
        """
        version = 'HTTP/1.1' if response.raw.version == 11 else 'HTTP/1.0'
        status_code = response.status_code
        reason = response.reason
        # hdDict = response.headers._store.items()
        headers = response.headers
        cookies = response.cookies
        body = response.raw.read()
        return cls(
            **dict(
                version=version,
                status_code=status_code,
                reason=reason,
                headers=headers,
                cookies=cookies,
                body=body
            )
        )

    def make_raw(self):
        """ makes byte string ready to pass to a socket """
        first_line = f'{self.version} {self.status_code} {self.reason}'.encode()
        hd_list = list(map(lambda x: f'{x[0]}: {x[1]}'.encode(), dict(self.headers).items()))
        headers = b'\r\n'.join(hd_list)
        if self.headers.get('transfer-encoding') == 'chunked':
            pass_body = b'%x\r\n%s\r\n0\r\n\r\n' % (len(self.body), self.body)
        else:
            pass_body = self.body
        return b'%s\r\n%s\r\n\r\n%s' % (first_line, headers, pass_body)

    def get_remote_host(self):
        """ remote gost saved in dialog """
        return self.dialog.remote_host

    def __str__(self):
        remote_host = self.get_remote_host()
        port = self.dialog.client_port
        line = f'{self.version} {self.status_code} {self.reason}'
        # headers = pretty_dict(self.headers)
        # pylint: disable=line-too-long
        # return f'resp from {remote_host} for {port}: {line}\nheaders: {headers}\ncookies: {self.cookies}\nbody length: {len(self.body)}\n\n'
        return f'resp from {remote_host} for {port}: {line}\n'
