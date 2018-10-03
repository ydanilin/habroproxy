import os
import socket
import select
from .read import readRequestLine, readHeaders
from .message import RequestDetails


def getLinesep():
    # must be always CRLF?
    return b'\r\n'  # if os.name == "nt" else b'\n'

def read(sock, pollInterval):
    rawMessage = b''
    while True:
        r, _, _ = select.select([sock], [], [], pollInterval)
        if sock in r:
            try:
                chunk = sock.recv(1024)
                rawMessage += chunk
            except socket.error:
                break  # TODO construct exeption
        else:
            break
    return rawMessage


class ReceiveService:

    def receive(self, sock, pollInterval=0.1):
        rawMessage = read(sock, pollInterval)
        lsep = getLinesep()
        print(rawMessage)
        request, *body = rawMessage.split(lsep + lsep, maxsplit=1)
        head, *tail = request.split(lsep)
        requestLineDict = readRequestLine(head)
        headers = readHeaders(tail)
        return RequestDetails(requestLineDict, headers, body)