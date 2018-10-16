"""
    Tool to create Habroproxy authority certificates.
    See readme for details
"""
import os
import time
import OpenSSL


DEFAULT_EXP = 94608000  # = 24 * 60 * 60 * 365 * 3
# Generated with "openssl dhparam". It's too slow to generate this on startup.
DEFAULT_DHPARAM = b"""
-----BEGIN DH PARAMETERS-----
MIICCAKCAgEAyT6LzpwVFS3gryIo29J5icvgxCnCebcdSe/NHMkD8dKJf8suFCg3
O2+dguLakSVif/t6dhImxInJk230HmfC8q93hdcg/j8rLGJYDKu3ik6H//BAHKIv
j5O9yjU3rXCfmVJQic2Nne39sg3CreAepEts2TvYHhVv3TEAzEqCtOuTjgDv0ntJ
Gwpj+BJBRQGG9NvprX1YGJ7WOFBP/hWU7d6tgvE6Xa7T/u9QIKpYHMIkcN/l3ZFB
chZEqVlyrcngtSXCROTPcDOQ6Q8QzhaBJS+Z6rcsd7X+haiQqvoFcmaJ08Ks6LQC
ZIL2EtYJw8V8z7C0igVEBIADZBI6OTbuuhDwRw//zU1uq52Oc48CIZlGxTYG/Evq
o9EWAXUYVzWkDSTeBH1r4z/qLPE2cnhtMxbFxuvK53jGB0emy2y1Ei6IhKshJ5qX
IB/aE7SSHyQ3MDHHkCmQJCsOd4Mo26YX61NZ+n501XjqpCBQ2+DfZCBh8Va2wDyv
A2Ryg9SUz8j0AXViRNMJgJrr446yro/FuJZwnQcO3WQnXeqSBnURqKjmqkeFP+d8
6mk2tqJaY507lRNqtGlLnj7f5RNoBFJDCLBNurVgfvq9TCVWKDIFD4vZRjCrnl6I
rD693XKIHUCWOjMh1if6omGXKHH40QuME2gNa50+YPn1iYDl88uDbbMCAQI=
-----END DH PARAMETERS-----
"""


def create_ca(organization, common_name, expiration):
    """
        Creates certificate agency and private key
    """
    p_key = OpenSSL.crypto.PKey()
    p_key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    ca_cert = OpenSSL.crypto.X509()
    ca_cert.set_serial_number(int(time.time() * 10000))
    ca_cert.set_version(2)
    ca_cert.get_subject().CN = common_name
    ca_cert.get_subject().O = organization
    ca_cert.gmtime_adj_notBefore(-3600 * 48)
    ca_cert.gmtime_adj_notAfter(expiration)
    ca_cert.set_issuer(ca_cert.get_subject())
    ca_cert.set_pubkey(p_key)
    ca_cert.add_extensions([
        OpenSSL.crypto.X509Extension(
            b"basicConstraints",
            True,
            b"CA:TRUE"
        ),
        OpenSSL.crypto.X509Extension(
            b"nsCertType",
            False,
            b"sslCA"
        ),
        OpenSSL.crypto.X509Extension(
            b"extendedKeyUsage",
            False,
            # pylint: disable=line-too-long
            b"serverAuth,clientAuth,emailProtection,timeStamping,msCodeInd,msCodeCom,msCTLSign,msSGC,msEFS,nsSGC"
        ),
        OpenSSL.crypto.X509Extension(
            b"keyUsage",
            True,
            b"keyCertSign, cRLSign"
        ),
        OpenSSL.crypto.X509Extension(
            b"subjectKeyIdentifier",
            False,
            b"hash",
            subject=ca_cert
        ),
    ])
    ca_cert.sign(p_key, "sha256")
    return p_key, ca_cert


def save_ca_pub_key(path_name, msg, **cakey):
    """ Dump the CA plus private key """
    with open(path_name, "wb") as f_handler:
        f_handler.write(
            OpenSSL.crypto.dump_privatekey(
                OpenSSL.crypto.FILETYPE_PEM,
                cakey['key']))
        f_handler.write(
            OpenSSL.crypto.dump_certificate(
                OpenSSL.crypto.FILETYPE_PEM,
                cakey['ca']))
        print(f'{msg}: {f_handler.name}')


def save_cert(path_name, msg, **cakey):
    """ Dump the certificate in PEM format """
    with open(path_name, "wb") as f_handler:
        f_handler.write(
            OpenSSL.crypto.dump_certificate(
                OpenSSL.crypto.FILETYPE_PEM,
                cakey['ca']))
        print(f'{msg}: {f_handler.name}')


def save_win_cert(path_name, msg, **cakey):
    """ Dump the certificate in PKCS12 format for Windows devices """
    with open(path_name, "wb") as f_handler:
        p12 = OpenSSL.crypto.PKCS12()
        p12.set_certificate(cakey['ca'])
        f_handler.write(p12.export())
        print(f'{msg}: {f_handler.name}')


def save_dh_params(path_name, msg, **cakey):  # pylint: disable=unused-argument
    """ https://security.stackexchange.com/questions/94390/whats-the-purpose-of-dh-parameters """
    with open(path_name, "wb") as f_handler:
        f_handler.write(DEFAULT_DHPARAM)
        print(f'{msg}: {f_handler.name}')


BASENAME = 'habroproxy'
ORG = 'Habroproxy Ltd.'
CA_PATH = os.path.join(os.curdir, 'cert')
NEEDED_CERTS = [
    {
        'msg': 'created CA PLUS private key file (to be used internally)',
        'path_name': os.path.join(CA_PATH, BASENAME + "-ca.pem"),
        'saveProc': save_ca_pub_key,
    },
    {
        'msg': 'created certificate file to install in clients',
        'path_name': os.path.join(CA_PATH, BASENAME + "-ca-cert.pem"),
        'saveProc': save_cert,
    },
    {
        'msg': 'created certificate file for Windows system store',
        'path_name': os.path.join(CA_PATH, BASENAME + "-ca-cert.p12"),
        'saveProc': save_win_cert,
    },
    {
        'msg': 'created Diffie-Hellman parameters file',
        'path_name': os.path.join(CA_PATH, BASENAME + "-dhparam.pem"),
        'saveProc': save_dh_params,
    },
]


if __name__ == '__main__':
    if not os.path.exists(NEEDED_CERTS[0]['path_name']):
        if not os.path.exists(CA_PATH):
            os.makedirs(CA_PATH)
        # pylint: disable=invalid-name
        key, ca = create_ca(organization=ORG, common_name=BASENAME, expiration=DEFAULT_EXP)
        for cert in NEEDED_CERTS:
            cert['saveProc'](cert['path_name'], cert['msg'], ca=ca, key=key)
    else:
        print('Already existing:')
        # We checked that only the first file (CA + priv key) exists
        # other just to dispaly names to the user
        for cert in NEEDED_CERTS:
            print(f'{cert["msg"]}: {cert["path_name"]}'.replace('created ', ''))
