import os
import socket
import select

def getLinesep():
    return b'\r\n' if os.name == "nt" else b'\n'

def read(sock, pollInterval):
    rawMessage = b''
    while True:
        r, _, _ = select.select([sock], [], [], pollInterval)
        if sock in r:
            try:
                chunk = sock.recv(1024)
                rawMessage += chunk
            except socket.error:
                break
        else:
            break
    return rawMessage


class ReceiveService:

    def receive(self, sock, pollInterval=0.1):
        # import pdb; pdb.set_trace()
        rawMessage = read(sock, pollInterval)
        lsep = getLinesep()
        head, body = rawMessage.split(lsep + lsep, maxsplit=1)
        headList = head.split(lsep)
        fline = headList[0]
        headers = headList[1:]
        return fline, headers

