import logging

def setup():
    FORMAT = "[ %(asctime)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=logging.INFO,format=FORMAT)
    log = logging.getLogger(__name__)
    return log
