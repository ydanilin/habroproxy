"""
    The service creates dummy certificate for a given domain.
    So the trust chain is our agency certificate -> dummy certificate.
    User must install habroproxy's agency certificate as trusted,
    see project readme for details.
"""
import time
import OpenSSL
from habroproxy.model.certs import CertificateAgency
from habroproxy.utils import get_cert_path


class TlsService:
    """ Spawns certificate agency with cert, privkey and dhparam loaded. """
    def __init__(self):
        self.agency = CertificateAgency(get_cert_path())

    def make_domain_cert(self, for_domain):
        """ Provides function to create dummy certificates """
        cert = OpenSSL.crypto.X509()
        cert.gmtime_adj_notBefore(-3600 * 48)
        cert.gmtime_adj_notAfter(63072000)  # 2 years ))
        cert.set_issuer(self.agency.cacert.get_subject())
        cert.get_subject().CN = for_domain
        cert.set_serial_number(int(time.time() * 10000))
        # cert extensions
        # Howewer, tests with browsers (Firefox Ubuntu, Windows) revealed
        # that there are much less SSL hanshake errors with client
        # when no subjectAltName extension enabled
        # ---- commented out start
        # cert.set_version(2)
        #asteriskForms = map(lambda x: b"DNS:%s" % x.encode(), self.get_asterisks_forms(for_domain))
        # cert.add_extensions(
        #     [OpenSSL.crypto.X509Extension(
        #         b"subjectAltName", False, b', '.join(asteriskForms)
        #     )]
        # )
        # ---- commented out end
        cert.set_pubkey(self.agency.cacert.get_pubkey())
        cert.sign(self.agency.get_priv_key(), "sha256")
        return cert

    def create_ssl_context(self, host):
        """ provides context with full trust path already installed """
        def accept_all(
                conn_,  #pylint: disable=unused-argument
                x509,  #pylint: disable=unused-argument
                errno,  #pylint: disable=unused-argument
                err_depth,  #pylint: disable=unused-argument
                is_cert_verified):  #pylint: disable=unused-argument
            # Return true to prevent cert verification error
            return True

        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        ctx.set_verify(0, accept_all)
        ctx.load_verify_locations(self.agency.get_agency_location())
        ctx.set_mode(OpenSSL.SSL._lib.SSL_MODE_AUTO_RETRY)
        cert = self.make_domain_cert(host)
        key = self.agency.get_priv_key()
        ctx.use_certificate(cert)
        ctx.use_privatekey(key)
        OpenSSL.SSL._lib.SSL_CTX_set_tmp_dh(ctx._context, self.agency.get_dh_param())
        return ctx


def get_asterisks_forms(for_domain):
    """ example.unl.edu -> *.unl.edu """
    parts = for_domain.split('.')
    output = [for_domain]
    for i in range(1, len(parts)):
        output.append('*.' + '.'.join(parts[i:]))
    return output
