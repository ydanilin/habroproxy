""" few methods to test cert using OpenSSL methods """
from habroproxy.services.tls import TlsService, get_asterisks_forms


REQUIRED_DOMAIN = 'habr.com'


def test_domain_cert():
    """ dummy cert CN must be required domain """
    tservice = TlsService()
    cert = tservice.make_domain_cert(REQUIRED_DOMAIN)
    assert cert.get_subject().CN == REQUIRED_DOMAIN


def test_ssl_context():
    """ private key checking must return None """
    tservice = TlsService()
    ctx = tservice.create_ssl_context(REQUIRED_DOMAIN)
    assert ctx.check_privatekey() is None


def test_asterisk_forms():
    """ for subject alt name extension """
    asterisk_forms = get_asterisks_forms(REQUIRED_DOMAIN)
    assert asterisk_forms == ['habr.com', '*.com']
