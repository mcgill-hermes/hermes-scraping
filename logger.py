import logging
from colorlog import ColoredFormatter
import constants


def init_logger():
    logging.basicConfig(level=logging.INFO,
                        format=constants.LOG_FORMAT_SIMPLE)
    formatter = ColoredFormatter(constants.LOG_FORMAT_FULL)
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    stream.setFormatter(formatter)
    logging.getLogger().addHandler(stream)

