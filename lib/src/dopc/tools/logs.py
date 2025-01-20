import os
import logging

loglevel = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'prod': logging.WARNING,
    'dev': logging.INFO,
    'debug': logging.DEBUG
}


def getConsoleLoger(name: str) -> logging.Logger:
    mainLogger = logging.getLogger(name)
    level = loglevel[os.getenv('env') or 'dev']
    mainLogger.setLevel(level=level)
    formatter = logging.Formatter('%(asctime)s | logger: %(name)s | line %(lineno)d  | \
                                  %(funcName)s %(filename)s| %(levelname)s: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level=level)
    stream_handler.setFormatter(formatter)
    if (mainLogger.hasHandlers()):
        mainLogger.handlers.clear()
    mainLogger.addHandler(stream_handler)
    return (mainLogger)
