""" standard libraries configuration module """
import os
import logging
from habroproxy.utils import get_log_path


# logging.basicConfig(level=logging.DEBUG)

LOG_LEVEL = logging.INFO


def configure(module_name):
    """ configure logging """
    log = logging.getLogger(module_name)
    log.propagate = False
    log.setLevel(logging.DEBUG)
    log_path = get_log_path()
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_name = os.path.join(log_path, f'{module_name}.log')
    f_handler = logging.FileHandler(file_name, mode='w')
    f_handler.setLevel(LOG_LEVEL)
    s_handler = logging.StreamHandler()
    s_handler.setLevel(LOG_LEVEL)
    log.addHandler(f_handler)
    log.addHandler(s_handler)
    return log
