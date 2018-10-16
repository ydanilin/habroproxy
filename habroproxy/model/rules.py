"""
    Contains Interceptor classes. Interceptors are things which modifies response bodies.
    They are to be supplied in a list to DialogService constructor, so
    the service will automatically invoke them on Response object one by one
    Every Interceptor must:
    - have intercept(response) method - this will be invoked by the service
    - encapsulate all criterias and data how to modify the response body
"""
from bs4 import BeautifulSoup, NavigableString, Comment
from habroproxy.utils import multi_insert, absent, decode_zip, encode_zip


COMPRESSORS = [
    {
        'name': 'gzip',
        'expand': decode_zip,
        'collapse': encode_zip,
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
    """
        Takes response body and appends tm_ sign to every word of char_count letters.
        Interceptor triggers based on the following criteria:
        - response host matches (contains) string of host argument
        - response content-type header is 'html'
        Other settings via __init__():
        - special: word delimiters, see habroproxy.utils multi_insert() description
        - ignored_tags: where multi_insert() must not look for words
    """
    def __init__(self, host):
        self.host = host
        # interceptor configuration
        self.content_type = 'html'
        self.tm_ = b'\xE2\x84\xA2'.decode()
        self.special = '"()- !.,?[]{}_\n\r\t:;'
        self.char_count = 6
        self.ignored_tags = ['script', 'code']

    def intercept(self, response):
        """
            The method which will be called by the service.
            MUTATES response body (returns nothing).
            Generally handles compression issues, delegates body modification to
            process() method
        """
        if not response.body:
            return
        will_process = (response.get_remote_host().find(self.host) > -1 and
                        response.headers.get('Content-type').find(self.content_type) > -1)
        if not will_process:
            return
        # modify body of the response
        compress_method = response.headers.get('content-encoding')
        if compress_method:
            compressor = list(filter(lambda x: x['name'] == compress_method, COMPRESSORS))[0]
            decoded = compressor['expand'](response.body)
            modified = self.process(decoded)
            response.body = compressor['collapse'](modified)
        else:
            modified = self.process(response.body)
            response.body = modified

    def process(self, content: bytes) -> bytes:
        """
            Focuses on pure content processing:
            - creates DOM tree
            - finds all leafs with pure text inside <body> tag
            - replaces that text with multi_insert processor output
        """
        soup = BeautifulSoup(content.decode('utf-8'), 'html5lib')
        nav_strings = filter(
            lambda x:
            isinstance(x, NavigableString)
            and x.parent.name not in self.ignored_tags
            and x.strip() != ''
            and not isinstance(x, Comment),
            soup.html.body.descendants
        )
        for ns_ in list(nav_strings):
            ns_.replace_with(multi_insert(ns_, self.tm_, self.char_count, self.special))
        return soup.encode()
