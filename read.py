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
    method, path, http_version = line.split()

    if path == b"*" or path.startswith(b"/"):
        form = "relative"
        scheme, host, port = None, None, None
    elif method == b"CONNECT":
        form = "authority"
        host, port = path.rsplit(b":", 1)
        scheme, path = None, None
    else:
        form = "absolute"
        scheme, host, port, path = parse(path)

    return form, method, scheme, host, port, path, http_version


def readHeaders(hlist):
    def f(acc, line):
        name, value = line.split(b":", 1)
        acc[name] = value = value.strip()
        return acc

    return reduce(f, hlist, OrderedDict())
