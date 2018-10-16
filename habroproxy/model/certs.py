""" represents our own certification agency """
import os
import sys
import OpenSSL


def load_dhparam(path):
    """ return dh ssl parameter """
    dhparam = None
    bio = OpenSSL.SSL._lib.BIO_new_file(path.encode(sys.getfilesystemencoding()), b"r")
    if bio != OpenSSL.SSL._ffi.NULL:
        bio = OpenSSL.SSL._ffi.gc(bio, OpenSSL.SSL._lib.BIO_free)
        dhparam = OpenSSL.SSL._lib.PEM_read_bio_DHparams(
            bio,
            OpenSSL.SSL._ffi.NULL,
            OpenSSL.SSL._ffi.NULL,
            OpenSSL.SSL._ffi.NULL)
        dhparam = OpenSSL.SSL._ffi.gc(dhparam, OpenSSL.SSL._lib.DH_free)
    return dhparam


class CertificateAgency:
    """
        loads agency certificate from <proj>/cert directory.
        a certificate file should be created prior to usage via
        /tools/gencert.py module. More information is in project readme
    """
    def __init__(self, ca_path):
        self.basename = 'habroproxy'
        self.ca_path = ca_path
        self.ca_file = os.path.join(self.ca_path, self.basename + '-ca.pem')
        try:
            with open(self.ca_file, "rb") as cafile:
                raw = cafile.read()
        except FileNotFoundError:
            # pylint: disable=line-too-long
            print(f'No certificate {self.ca_file} found. Did you generate it via /tools/gencert.py?')
            sys.exit(1)
        self.cacert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM,
            raw)
        self.priv_key = OpenSSL.crypto.load_privatekey(
            OpenSSL.crypto.FILETYPE_PEM,
            raw)
        self.dh_param = load_dhparam(os.path.join(self.ca_path, self.basename + '-dhparam.pem'))

    def get_ca_cert(self):
        """ returns agency certificate instance """
        return self.cacert

    def get_priv_key(self):
        """ returns private key loaded from agency certificate """
        return self.priv_key

    def get_dh_param(self):
        """ returns created dh param """
        return self.dh_param

    def get_agency_location(self):
        """ path to the agency directory """
        return self.ca_file
