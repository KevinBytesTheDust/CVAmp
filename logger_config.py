import logging
import os


def setup():

    handlers = [logging.FileHandler("ctvb.log", mode='w')]

    if os.getenv("DEBUG"):
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s;%(levelname)s;%(threadName)s;%(module)s;%(funcName)s; %(message)s',
        handlers=handlers,
    )
