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
