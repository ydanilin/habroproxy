import os
from habroproxy.utils import getCertPath, prettyDict, strHasDigits, multiInsert


def test_cert_path():
    path = getCertPath()
    assert os.path.exists(os.path.join(path, 'habroproxy-ca.pem')), True


def test_str_has_digits():
    ts1 = '100500.7'
    ts2 = 'Kitten13'
    ts3 = 'habroproxy'
    assert strHasDigits(ts1) == True
    assert strHasDigits(ts2) == True
    assert strHasDigits(ts3) == False


def test_multi_insert():
    tm = b'\xE2\x84\xA2'.decode()
    special = '"()- !.,?[]{}_\n\r\t:;'

    # started from separator and \r\n
    t_in1 = ('__ _ _\r\nОднако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
        'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.')
    t_out1 = ('__ _ _\r\nОднако™, в последнюю? "модель™" (автомобиля)  ,   .  установили необычный-необычный device™-аппарат.'
        'Данный™ аппарат уме8ет вырабатывать 10500т топлива буквально из ничего™.')
    assert multiInsert(t_in1, tm, 6, special) == t_out1

    # started from separator and \r\n after a word
    t_in2 = ('__ _ _Однако\r\n, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
        'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.')
    t_out2 = ('__ _ _Однако™\r\n, в последнюю? "модель™" (автомобиля)  ,   .  установили необычный-необычный device™-аппарат.'
        'Данный™ аппарат уме8ет вырабатывать 10500т топлива буквально из ничего™.')
    assert multiInsert(t_in2, tm, 6, special) == t_out2

    # started from word
    t_in3 = ('Однако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
        'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.       ')
    t_out3 = ('Однако™, в последнюю? "модель™" (автомобиля)  ,   .  установили необычный-необычный device™-аппарат.'
        'Данный™ аппарат уме8ет вырабатывать 10500т топлива буквально из ничего™.       ')
    assert multiInsert(t_in3, tm, 6, special) == t_out3

    # should leave unchanged
    t_in4 = ('Однако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
        'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.       ')
    t_out4 = ('Однако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
        'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.       ')
    assert multiInsert(t_in4, tm, 88, special) == t_out4
