""" Test utility functions from utils.py """
from habroproxy.utils import str_has_digits, multi_insert


def test_str_has_digits():
    """ This is for TMInterceptor """
    ts1 = '100500.7'
    ts2 = 'Kitten13'
    ts3 = 'habroproxy'
    assert str_has_digits(ts1) is True
    assert str_has_digits(ts2) is True
    assert str_has_digits(ts3) is False


def test_multi_insert():
    """
        This test illustrates how TMInterceptor work
    """
    trademark = b'\xE2\x84\xA2'.decode()
    special = '"()- !.,?[]{}_\n\r\t:;'

    # started from separator and \r\n
    # pylint: disable=line-too-long
    t_in1 = ('__ _ _\r\nОднако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
             'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.')
    # pylint: disable=line-too-long
    t_out1 = ('__ _ _\r\nОднако™, в последнюю? "модель™" (автомобиля)  ,   .  установили необычный-необычный device™-аппарат.'
              'Данный™ аппарат уме8ет вырабатывать 10500т топлива буквально из ничего™.')
    assert multi_insert(t_in1, trademark, 6, special) == t_out1

    # started from separator and \r\n after a word
    # pylint: disable=line-too-long
    t_in2 = ('__ _ _Однако\r\n, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
             'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.')
    # pylint: disable=line-too-long
    t_out2 = ('__ _ _Однако™\r\n, в последнюю? "модель™" (автомобиля)  ,   .  установили необычный-необычный device™-аппарат.'
              'Данный™ аппарат уме8ет вырабатывать 10500т топлива буквально из ничего™.')
    assert multi_insert(t_in2, trademark, 6, special) == t_out2

    # started from word
    # pylint: disable=line-too-long
    t_in3 = ('Однако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
             'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.       ')
    # pylint: disable=line-too-long
    t_out3 = ('Однако™, в последнюю? "модель™" (автомобиля)  ,   .  установили необычный-необычный device™-аппарат.'
              'Данный™ аппарат уме8ет вырабатывать 10500т топлива буквально из ничего™.       ')
    assert multi_insert(t_in3, trademark, 6, special) == t_out3

    # should leave unchanged
    # pylint: disable=line-too-long
    t_in4 = ('Однако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
             'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.       ')
    # pylint: disable=line-too-long
    t_out4 = ('Однако, в последнюю? "модель" (автомобиля)  ,   .  установили необычный-необычный device-аппарат.'
              'Данный аппарат уме8ет вырабатывать 10500т топлива буквально из ничего.       ')
    assert multi_insert(t_in4, trademark, 88, special) == t_out4
