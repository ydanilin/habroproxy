import os
from habroproxy.utils import getCertPath, prettyDict


def test_cert_path():
    path = getCertPath()
    assert os.path.exists(os.path.join(path, 'habroproxy-ca.pem')), True

def test_pretty_dict():
    dic = {
        'Host': 'habr.com',
        'User-Agent': 'python-requests/2.19.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    output = prettyDict(dic, 1)
    needed = """         Host: habr.com
         User-Agent: python-requests/2.19.1
"""
    # assert output == needed
