import logging
import sys


def init_logging(log_level: int):
    root = logging.getLogger()
    root.setLevel(log_level)
    handler = logging.FileHandler('log.log', 'w+')
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(funcName)20s() - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logconsole = logging.StreamHandler()
    logconsole.setLevel(log_level)
    logconsole.setFormatter(formatter)
    logging.root.addHandler(logconsole)
    root.addHandler(handler)

