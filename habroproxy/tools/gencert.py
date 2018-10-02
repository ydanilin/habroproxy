import os
import OpenSSL
import time


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


def create_ca(o, cn, exp):
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    cert = OpenSSL.crypto.X509()
    cert.set_serial_number(int(time.time() * 10000))
    cert.set_version(2)
    cert.get_subject().CN = cn
    cert.get_subject().O = o
    cert.gmtime_adj_notBefore(-3600 * 48)
    cert.gmtime_adj_notAfter(exp)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.add_extensions([
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
            subject=cert
        ),
    ])
    cert.sign(key, "sha256")
    return key, cert


def saveCaPubKey(pathName, msg, **cakey):
    # Dump the CA plus private key
    with open(pathName, "wb") as f:
        f.write(
            OpenSSL.crypto.dump_privatekey(
                OpenSSL.crypto.FILETYPE_PEM,
                cakey['key']))
        f.write(
            OpenSSL.crypto.dump_certificate(
                OpenSSL.crypto.FILETYPE_PEM,
                cakey['ca']))
        print(f'{msg}: {f.name}')


def saveCert(pathName, msg, **cakey):
    # Dump the certificate in PEM format
    with open(pathName, "wb") as f:
        f.write(
            OpenSSL.crypto.dump_certificate(
                OpenSSL.crypto.FILETYPE_PEM,
                cakey['ca']))
        print(f'{msg}: {f.name}')


def saveWinCert(pathName, msg, **cakey):
    # Dump the certificate in PKCS12 format for Windows devices
    with open(pathName, "wb") as f:
        p12 = OpenSSL.crypto.PKCS12()
        p12.set_certificate(cakey['ca'])
        f.write(p12.export())
        print(f'{msg}: {f.name}')


def saveDHParams(pathName, msg, **cakey):
    # https://security.stackexchange.com/questions/94390/whats-the-purpose-of-dh-parameters
    with open(pathName, "wb") as f:
        f.write(DEFAULT_DHPARAM)
        print(f'{msg}: {f.name}')


if __name__ == '__main__':
    basename = 'habroproxy'
    org = 'Habroproxy Ltd.'
    ca_path = os.path.join(os.curdir, 'cert')
    neededCerts = [
        {
            'msg': 'created CA PLUS private key file (to be used internally)',
            'pathName': os.path.join(ca_path, basename + "-ca.pem"),
            'saveProc': saveCaPubKey,
        },
        {
            'msg': 'created certificate file to install in clients',
            'pathName': os.path.join(ca_path, basename + "-ca-cert.pem"),
            'saveProc': saveCert,
        },
        {
            'msg': 'created certificate file for Windows system store',
            'pathName': os.path.join(ca_path, basename + "-ca-cert.p12"),
            'saveProc': saveWinCert,
        },
        {
            'msg': 'created Diffie-Hellman parameters file',
            'pathName': os.path.join(ca_path, basename + "-dhparam.pem"),
            'saveProc': saveDHParams,
        },
    ]

    if not os.path.exists(neededCerts[0]['pathName']):
        if not os.path.exists(ca_path):
            os.makedirs(ca_path)
        key, ca = create_ca(o=org, cn=basename, exp=DEFAULT_EXP)
        for cert in neededCerts:
            cert['saveProc'](cert['pathName'], cert['msg'], ca=ca, key=key)
    else:
        print('Already existing:')
        # We checked that only the first file (CA + priv key) exists
        # other just to dispaly names to the user
        for cert in neededCerts:
            print(f'{cert["msg"]}: {cert["pathName"]}'.replace('created ', ''))
