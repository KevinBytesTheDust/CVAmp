import logging

def setup():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s;%(levelname)s;%(threadName)s;%(module)s;%(funcName)s; %(message)s',
                        handlers=[logging.FileHandler("ctvb.log", mode='a'),
                                  logging.StreamHandler()])


