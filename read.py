import urllib.parse
from collections import OrderedDict
from functools import reduce


def parse(path):
    parsed = urllib.parse.urlparse(path)
    scheme = parsed.scheme
    host = parsed.hostname
    if not parsed.port:
        port = 443 if scheme == b"https" else 80
    else:
        port = parsed.port
    full_path = urllib.parse.urlunparse(
        (b"", b"", parsed.path, parsed.params, parsed.query, parsed.fragment)
    )
    if not full_path.startswith(b"/"):
        full_path = b"/" + full_path
    return scheme, host, port, full_path


def readRequestLine(line):
    """
    return form, method, scheme, host, port, path, http_version
    """
    method, path, http_version = line.split()

    if path == b"*" or path.startswith(b"/"):
        return dict(
            form='relative',
            method=method,
            scheme=None,
            host=None,
            port=None,
            path=path,
            http_version=http_version
            )
    elif method == b"CONNECT":
        host, *port = path.rsplit(b":", 1)
        return dict(
            form='authority',
            method=method,
            scheme=None,
            host=host,
            port=port if port else 443,
            path=None,
            http_version=http_version
            )
    else:
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


def readHeaders(hlist):
    def f(acc, line):
        name, value = line.split(b":", 1)
        acc[name] = value = value.strip()
        return acc

    return reduce(f, hlist, OrderedDict())
