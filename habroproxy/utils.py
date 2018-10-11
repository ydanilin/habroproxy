import os
from itertools import zip_longest, chain
from io import BytesIO
import gzip


def iterPath(path, end=''):
    if end == 'habroproxy':
        return path, end
    elif path == '':
        return '', ''
    head, tail = os.path.split(path)
    return iterPath(head, tail)


def getCertPath():
    abs = os.path.abspath(os.curdir)
    root, proj = iterPath(abs)
    return os.path.join(root, proj, 'cert')


def getLogPath():
    abs = os.path.abspath(os.curdir)
    root, proj = iterPath(abs)
    return os.path.join(root, proj, 'log')


def prettyDict(d, indent=1):
    spaces = 9
    fill = ' ' * spaces * indent
    output = []
    for key, value in d.items():
       if isinstance(value, dict):
            output.append(f'{fill}{key}:')
            prettyDict(value, indent+1)
       else:
            output.append(f'{fill}{key}: {value}')
    return '\n'.join(output).replace(fill, '', 1)


def strHasDigits(s):
    return any(map(lambda x: x.isdigit(), s))


def insertIfNeeded(what, condLen):
    return lambda word: f'{word}{what}' if len(word) == condLen and not strHasDigits(word) else word


def multiInsert(stri, what, condLen, special):
    """
        Inserts <what> at the end of every word in the <stri> if the length of this word is <condLen> characters.
        Which symbols will be used as separators defined in <special> string.
        Example is in test_utils.py

    """
    word = ''
    words = []
    separ = ''
    separs = []
    # peek into the string to set start state
    state = 'inside' if stri[0] not in special else 'outside'
    initialState = state
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
    modifiedWords = map(insertIfNeeded(what, condLen), words)
    zipBack = (modifiedWords, separs) if initialState == 'inside' else (separs, modifiedWords)
    reconstructed = chain(*zip_longest(*zipBack, fillvalue=''))
    return ''.join(reconstructed)


def absent():
    raise NotImplementedError()


def decodeZip(source):
    if not source:
        return b""
    gfile = gzip.GzipFile(fileobj=BytesIO(source))
    return gfile.read()


def encodeZip(source):
    s = BytesIO()
    gf = gzip.GzipFile(fileobj=s, mode='wb')
    gf.write(source)
    gf.close()
    return s.getvalue()