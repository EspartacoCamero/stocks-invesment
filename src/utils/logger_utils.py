import logging
from datetime import datetime
import os


def log_creator(log_path: str, file_log_level=None, console_log_level=None, log_name: str = 'log_info') -> logging.Logger:
    """ Create custom logger
    """

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    if file_log_level is None:
        file_log_level = logging.DEBUG

    if console_log_level is None:
        console_log_level = logging.DEBUG

    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    name = os.path.join(log_path, "_".join([log_name, datetime.now().strftime("%Y%m%d_%H%M")+".log"]))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(name)
    fh.setLevel(file_log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(console_log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def module_logger_creator(logger_level):
    """ Create custom logger for modules
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logger_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logger_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
