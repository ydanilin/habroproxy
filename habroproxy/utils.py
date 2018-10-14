"""
    Most important part here is multi_insert() function for interceptor
    (see habroproxy/model/rules.py and project readme for details)
    Other stuff is misc utility functions
    like paths, pretty prints for loggers, dealing with gzip etc.
"""
import os
from itertools import zip_longest, chain
from io import BytesIO
import gzip


PROJECT_ROOT = 'habroproxy'


def iter_path(path, needed_name, end=''):
    """
        Iterates on path until folder needed_name found.
        Returns (path to that name, name).
        Example: '/home/user/dev/pitonizm/habroproxy/habroproxy/utils.py', 'pitonizm' ->
        ('/home/user/dev/', 'pitonizm')
    """
    if end == needed_name:
        return path, end
    if path == '':
        return '', ''
    head, tail = os.path.split(path)
    return iter_path(head, needed_name, tail)


def get_cert_path():
    """ Path to store certificate files: <project folder>/cert"""
    abs_ = os.path.abspath(os.curdir)
    root, proj = iter_path(abs_, PROJECT_ROOT)
    return os.path.join(root, proj, 'cert')


def get_log_path():
    """ Path to store logs: <project folder>/log"""
    abs_ = os.path.abspath(os.curdir)
    root, proj = iter_path(abs_, PROJECT_ROOT)
    return os.path.join(root, proj, 'log')


def pretty_dict(dict_, indent=1):
    """ used to pretty print request headers """
    spaces = 9
    fill = ' ' * spaces * indent
    output = []
    for key, value in dict_.items():
        if isinstance(value, dict):
            output.append(f'{fill}{key}:')
            pretty_dict(value, indent+1)
        else:
            output.append(f'{fill}{key}: {value}')
    return '\n'.join(output).replace(fill, '', 1)


def str_has_digits(stream):
    """ to check if a word has digits inside """
    return any(map(lambda x: x.isdigit(), stream))


def insert_if_needed(what, cond_len):
    """ Appends <what> to the end of a word if word length is <cond_len>"""
    # pylint: disable=line-too-long
    return lambda word: f'{word}{what}' if len(word) == cond_len and not str_has_digits(word) else word


def multi_insert(stri, what, cond_len, special):
    """
        Inserts <what> at the end of every word in the <stri> if
        the length of this word is <cond_len> characters.
        Which symbols will be used as separators defined in <special> string.
        Example is in test_utils.py
    """
    word = ''
    words = []
    separ = ''
    separs = []
    # peek into the string to set start state
    state = 'inside' if stri[0] not in special else 'outside'
    initial_state = state
    for char in stri:
        if state == 'inside':
            if char not in special:
                word += char
            else:
                separ += char
                words.append(word)
                word = ''
                state = 'outside'
        elif state == 'outside':
            if char in special:
                separ += char
            else:
                word += char
                separs.append(separ)
                separ = ''
                state = 'inside'
    # inclusion of last accumulator variable (word or separ) after cycle complete
    if state == 'inside':
        words.append(word)
    elif state == 'outside':
        separs.append(separ)
    # modification
    modified_words = map(insert_if_needed(what, cond_len), words)
    zip_back = (modified_words, separs) if initial_state == 'inside' else (separs, modified_words)
    reconstructed = chain(*zip_longest(*zip_back, fillvalue=''))
    return ''.join(reconstructed)


def absent():
    """ insert when function is not implemented """
    raise NotImplementedError()


def decode_zip(source):
    """ to un-gzip """
    if not source:
        return b""
    gfile = gzip.GzipFile(fileobj=BytesIO(source))
    return gfile.read()


def encode_zip(source):
    """ to gzip """
    stream = BytesIO()
    gzipfile = gzip.GzipFile(fileobj=stream, mode='wb')
    gzipfile.write(source)
    gzipfile.close()
    return stream.getvalue()
