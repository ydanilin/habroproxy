import os
import requests
import select
import ssl
from OpenSSL import SSL
from certs import CertificateService


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


class SendService:

    def sendToRemote(self, rd):
        resp = requests.request(
            rd.method,
            rd.getUrl(),
            headers = rd.headers,
            data = rd.body,
            stream=True
            )
        return resp

    def sendToClient(self, sock, response):
        version = b'HTTP/1.1' if response.raw.version == 11 else b'HTTP/1.0'
        statusCode = str(response.status_code).encode()
        reason = response.reason.encode()
        hdList = list(map(lambda x: f'{x[1][0]}: {x[1][1]}'.encode(), response.headers._store.items()))
        firstLine = b"%s %s %s" % (version, statusCode, reason)
        headers = b'\r\n'.join(hdList)
        # http://docs.python-requests.org/en/master/user/quickstart/#raw-response-content
        # https://docs.python.org/3.6/library/http.client.html#http.client.HTTPResponse
        body = response.raw.read()
        if response.headers.get('transfer-encoding') == 'chunked':
            passBody = b'%x\r\n%s\r\n0\r\n\r\n' % (len(body), body)
        else:
            passBody = body
        httpText = b'%s\r\n%s\r\n\r\n%s' % (firstLine, headers, passBody)
        return sock.send(httpText)

    def convertToTls(self, sock, connRequest):
        def accept_all(
            conn_: SSL.Connection,
            x509: SSL.X509,
            errno: int,
            err_depth: int,
            is_cert_verified: bool):
                # Return true to prevent cert verification error
                return True

        text = b'%s %d %s\r\n\r\n' % (
            connRequest.http_version.encode(), 200, b'Connection established')
        sock.sendall(text)

        certService = CertificateService()

        ctx = SSL.Context(SSL.SSLv23_METHOD)
        # ctx = SSL.Context(SSL.TLSv1_2_METHOD)
        ctx.set_verify(0, accept_all)
        # do we need this? what is locations file?
        ctx.load_verify_locations(certService.caFile)
        ctx.set_mode(SSL._lib.SSL_MODE_AUTO_RETRY)
        # ctx.set_options(SSL.OP_NO_SSLv2)
        # ctx.set_options(SSL.OP_NO_SSLv3)
        cert, key = certService.makeDomainCert('habr.com')
        ctx.use_privatekey(key)
        ctx.use_certificate(cert)
        SSL._lib.SSL_CTX_set_tmp_dh(ctx._context, certService.DHParam)

        ss = SSL.Connection(ctx, sock)
        ss.set_accept_state()
        try:
            ss.do_handshake()
        except SSL.Error as v:
            print("SSL handshake error: %s" % repr(v))
        return ss
        