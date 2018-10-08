from habroproxy.services.tls import TlsService


def test_domain_cert():
    requiredDomain = 'habr.com'
    tservice = TlsService()
    cert = tservice.makeDomainCert(requiredDomain)
    assert cert.get_subject().CN == requiredDomain

def test_ssl_context():
    requiredDomain = 'habr.com'
    tservice = TlsService()
    ctx = tservice.createSslContext(requiredDomain)
    assert ctx.check_privatekey() == None

def test_asterisk_forms():
    requiredDomain = 'habr.com'
    tservice = TlsService()
    asteriskForms = tservice.getAsteriskForms(requiredDomain)
    assert asteriskForms == ['habr.com', '*.com']
