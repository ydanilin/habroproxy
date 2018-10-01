import os
import sys
import time
import OpenSSL


def loadDhparam(path):
    bio = OpenSSL.SSL._lib.BIO_new_file(path.encode(sys.getfilesystemencoding()), b"r")
    if bio != OpenSSL.SSL._ffi.NULL:
        bio = OpenSSL.SSL._ffi.gc(bio, OpenSSL.SSL._lib.BIO_free)
        dh = OpenSSL.SSL._lib.PEM_read_bio_DHparams(
            bio,
            OpenSSL.SSL._ffi.NULL,
            OpenSSL.SSL._ffi.NULL,
            OpenSSL.SSL._ffi.NULL)
        dh = OpenSSL.SSL._ffi.gc(dh, OpenSSL.SSL._lib.DH_free)
        return dh


class CertificateService:
    def __init__(self):
        self.basename = 'habroproxy'
        self.caPath = os.path.join(os.curdir, 'cert')
        self.caFile = os.path.join(self.caPath, self.basename + '-ca.pem')
        with open(self.caFile, "rb") as f:
            raw = f.read()
        self.cacert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM,
            raw)
        self.privKey = OpenSSL.crypto.load_privatekey(
            OpenSSL.crypto.FILETYPE_PEM,
            raw)
        self.DHParam = loadDhparam(os.path.join(self.caPath, self.basename + '-dhparam.pem'))

    def makeDomainCert(self, forDomain):
        cert = OpenSSL.crypto.X509()
        cert.gmtime_adj_notBefore(-3600 * 48)
        cert.gmtime_adj_notAfter(63072000)  # 2 years ))
        cert.set_issuer(self.cacert.get_subject())
        cert.get_subject().CN = forDomain
        cert.set_serial_number(int(time.time() * 10000))
        cert.set_pubkey(self.cacert.get_pubkey())
        cert.sign(self.privKey, "sha256")
        return cert, self.privKey
