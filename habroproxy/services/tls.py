import time
import OpenSSL
from habroproxy.model.certs import CertificateAgency
from habroproxy.utils import getCertPath


class TlsService:
    def __init__(self):
        self.ca = CertificateAgency(getCertPath())

    def makeDomainCert(self, forDomain):
        cert = OpenSSL.crypto.X509()
        cert.gmtime_adj_notBefore(-3600 * 48)
        cert.gmtime_adj_notAfter(63072000)  # 2 years ))
        cert.set_issuer(self.ca.cacert.get_subject())
        cert.get_subject().CN = forDomain
        cert.set_serial_number(int(time.time() * 10000))
        cert.set_pubkey(self.ca.cacert.get_pubkey())
        cert.sign(self.ca.privKey, "sha256")
        return cert

    def getPrivateKey(self):
        return self.ca.privKey

    def getAgencyFilePath(self):
        return self.ca.caFile

    def getDHParam(self):
        return self.ca.DHParam

    def createSslContext(self, host):
        def accept_all(
            conn_: OpenSSL.SSL.Connection,
            x509: OpenSSL.SSL.X509,
            errno: int,
            err_depth: int,
            is_cert_verified: bool):
                # Return true to prevent cert verification error
                return True

        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        ctx.set_verify(0, accept_all)
        ctx.load_verify_locations(self.getAgencyFilePath())
        ctx.set_mode(OpenSSL.SSL._lib.SSL_MODE_AUTO_RETRY)
        cert = self.makeDomainCert(host)
        key = self.getPrivateKey()
        ctx.use_certificate(cert)
        ctx.use_privatekey(key)
        OpenSSL.SSL._lib.SSL_CTX_set_tmp_dh(ctx._context, self.getDHParam())
        return ctx
