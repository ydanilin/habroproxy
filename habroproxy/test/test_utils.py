import os
from habroproxy.utils import getCertPath


def test_cert_path():
    path = getCertPath()
    assert os.path.exists(os.path.join(path, 'habroproxy-ca.pem')), True
