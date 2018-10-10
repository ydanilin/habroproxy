from itertools import zip_longest, chain


special = '"()- !.,?[]{}_\n\r\t'
tm = b'\xE2\x84\xA2'.decode()


def strHasDigits(s):
    return any(map(lambda x: x.isdigit(), s))


def multiInsert(stri, what, condLen):
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


def insertIfNeeded(what, condLen):
    return lambda word: f'{word}{what}' if len(word) == condLen and not strHasDigits(word) else word


if __name__ == '__main__':
    ts = ('__ _ _\r\nОднако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
    'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.')
    ts1 = multiInsert(ts, tm, 6)
    print(ts1)
