import logging
import sys


def init_logging(log_level: int):
    root = logging.getLogger()
    root.setLevel(log_level)
    handler = logging.FileHandler('log.log', 'w+')
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logconsole = logging.StreamHandler()
    logconsole.setLevel(log_level)
    logconsole.setFormatter(formatter)
    logging.root.addHandler(logconsole)
    root.addHandler(handler)


#
# def logging_config(name=None, level=logging.DEBUG, console_level=logging.DEBUG):
#     if name is None:
#         name = inspect.stack()[1][1].split('.')[0]
#     folder = os.path.join(os.getcwd(), name)
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     logpath = os.path.join(folder, name + ".log")
#     print("All Logs will be saved to %s"  %logpath)
#     logging.root.setLevel(level)
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     logfile = logging.FileHandler(logpath)
#     logfile.setLevel(level)
#     logfile.setFormatter(formatter)
#     logging.root.addHandler(logfile)
#     #TODO Update logging patterns in other files
#     logconsole = logging.StreamHandler()
#     logconsole.setLevel(console_level)
#     logconsole.setFormatter(formatter)
#     logging.root.addHandler(logconsole)
#     return folder