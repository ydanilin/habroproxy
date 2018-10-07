import os
import logging
from habroproxy.utils import getLogPath


# logging.basicConfig(level=logging.DEBUG)


def configure(moduleName):
    log = logging.getLogger(moduleName)
    log.setLevel(logging.DEBUG)
    logPath = getLogPath()
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    fileName = os.path.join(logPath, f'{moduleName}.log')
    fh = logging.FileHandler(fileName, mode='w')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(fh)
    log.addHandler(ch)
    return log
