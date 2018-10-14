""" functions to parse various raw http text parts """
import urllib.parse
from collections import OrderedDict
from functools import reduce

def lsep():
    """
        As per standard, http protocol messages should use \r\n as separator
        Left as separate function for possible compatibility issues
    """
    return b'\r\n'

def parse(path):
    """ parses request line for scheme, host, port, full_path """
    parsed = urllib.parse.urlparse(path)
    scheme = parsed.scheme
    host = parsed.hostname
    if not parsed.port:
        port = '443' if scheme == "https" else '80'
    else:
        port = parsed.port
    full_path = urllib.parse.urlunparse(
        ("", "", parsed.path, parsed.params, parsed.query, parsed.fragment)
    )
    if not full_path.startswith("/"):
        full_path = "/" + full_path
    return scheme, host, port, full_path


def read_request_line(line):
    """
        return form, method, scheme, host, port, path, http_version
    """
    method, path, http_version = line.decode().split()

    if path == "*" or path.startswith("/"):
        return dict(
            form='relative',
            method=method,
            # scheme=None,
            # host=None,
            # port=None,
            path=path,
            http_version=http_version
            )
    if method == "CONNECT":
        host, port = path.rsplit(":", 1)
        return dict(
            form='authority',
            method=method,
            # scheme=None,
            host=host,
            port=port if port else '443',
            # path=None,
            http_version=http_version
            )
    scheme, host, port, path = parse(path)
    return dict(
        form='absolute',
        method=method,
        scheme=scheme,
        host=host,
        port=port,
        path=path,
        http_version=http_version
        )


def read_headers(hlist):
    """ simple headers extraction procedure """
    def f(acc, line):  # pylint: disable=invalid-name
        """ For reduce. We miss arrow functions in Python... """
        name, value = line.split(b":", 1)
        acc[name.decode()] = value.decode().strip()
        return acc

    return reduce(f, hlist, OrderedDict())
