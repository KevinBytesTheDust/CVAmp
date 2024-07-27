import logging
import os

import psutil


def setup():
    import sys

    print(sys.argv[0])

    handlers = [logging.FileHandler("cvamp.log", mode="w")]

    if os.getenv("DEBUG"):
        print("DEBUG ON")
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s;%(levelname)s;%(HWUsage)s;%(threadName)s;%(module)s;%(funcName)s;%(message)s",
        handlers=handlers,
    )

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.HWUsage = f"{psutil.cpu_percent(interval=None):.0f}_{psutil.virtual_memory().percent:.0f}"
        return record

    logging.setLogRecordFactory(record_factory)
