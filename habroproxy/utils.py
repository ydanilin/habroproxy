import os


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
