from bs4 import BeautifulSoup, NavigableString, Comment
from habroproxy.utils import multiInsert, absent, decodeZip, encodeZip


compressors = [
    {
        'name': 'gzip',
        'expand': decodeZip,
        'collapse': encodeZip,
    },
    {
        'name': 'deflate',
        'expand': absent,
        'collapse': absent,
    },
    {
        'name': 'br',
        'expand': absent,
        'collapse': absent,
    },
    {
        'name': 'identity',
        'expand': lambda x: x,
        'collapse': lambda x: x
    },
]


class TMInterceptor:
    def __init__(self, host):
        self.host = host
        # interceptor configuration
        self.content_type = 'html'
        self.tm = b'\xE2\x84\xA2'.decode()
        self.special = '"()- !.,?[]{}_\n\r\t:;'
        self.charCount = 6
        self.ignoredTags = ['script', 'code']

    def intercept(self, response):
        if not response.body:
            return
        willProcess = (response.getRemoteHost().find(self.host) > -1 and
            response.headers.get('Content-type').find(self.content_type) > -1)
        if not willProcess:
            return
        # modify body of the response
        compressMethod = response.headers.get('content-encoding')
        if compressMethod:
            compressor = list(filter(lambda x: x['name'] == compressMethod, compressors))[0]
            decoded = compressor['expand'](response.body)
            modified = self.process(decoded)
            response.body = compressor['collapse'](modified)
        else:
            modified = self.process(response.body)
            response.body = modified

    def process(self, content: bytes) -> bytes:
        soup = BeautifulSoup(content.decode('utf-8'), 'lxml')
        navStrings = filter(
            lambda x:
                isinstance(x, NavigableString)
                and x.parent.name not in self.ignoredTags
                and x.strip() != ''
                and not isinstance(x, Comment),
            soup.html.body.descendants
        )
        for ns in list(navStrings):
            ns.replace_with(multiInsert(ns, self.tm, self.charCount, self.special))
        return soup.encode()
