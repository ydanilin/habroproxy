""" standard libraries configuration module """
import os
import logging
from habroproxy.utils import get_log_path


# logging.basicConfig(level=logging.DEBUG)


def configure(module_name):
    """ configure logging """
    log = logging.getLogger(module_name)
    log.setLevel(logging.DEBUG)
    log_path = get_log_path()
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_name = os.path.join(log_path, f'{module_name}.log')
    f_handler = logging.FileHandler(file_name, mode='w')
    f_handler.setLevel(logging.DEBUG)
    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.DEBUG)
    log.addHandler(f_handler)
    log.addHandler(s_handler)
    return log
