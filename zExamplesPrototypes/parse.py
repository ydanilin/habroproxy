import os
from bs4 import BeautifulSoup
from bs4 import NavigableString, Comment
from habroproxy.utils import multiInsert
# *****************************************
# to execute, do python -m zExamplesPrototypes.parse
# from root project directory
# *****************************************


tm = b'\xE2\x84\xA2'.decode()
special = '"()- !.,?[]{}_\n\r\t:;'

ignoredTags = ['script', 'code']
# digits inside a word = ignore
# \r\n in text start


def iterPath(path, end=''):
    if end == 'habroproxy':
        return path, end
    elif path == '':
        return '', ''
    head, tail = os.path.split(path)
    return iterPath(head, tail)

if __name__ == '__main__':
    fullPath = os.path.dirname(os.path.abspath(__file__))
    fileName = os.path.join(fullPath, 'lagrange.htm')
    f = open(fileName, 'rb')
    content = f.read()
    f.close()
    soup = BeautifulSoup(content.decode('utf-8'), 'lxml')
    navStrings = filter(
        lambda x:
            isinstance(x, NavigableString)
            and x.parent.name not in ignoredTags
            and x.strip() != ''
            and not isinstance(x, Comment),
        soup.html.body.descendants
    )

    for ns in list(navStrings):
        ns.replace_with(multiInsert(ns, tm, 6, special))
    fout = open(os.path.join(fullPath, 'lagr.htm'), 'wb')
    fout.write(soup.encode())
    fout.close()
