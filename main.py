import atexit
import multiprocessing
import logging
import os
import shutil
import sys

import flask

from app import app
import worker
import config


def startup():
    """
    Create working directory for workers
    :return:
    """
    if os.path.exists('tmp'):
        shutil.rmtree('tmp')

    os.mkdir('tmp')

    if not os.path.exists('logs'):
        os.mkdir('logs')


def shutdown():
    print('at exit')
    app.mp_queue.put('die')


def setup_logger():
    logger = multiprocessing.get_logger()
    handler = logging.FileHandler('logs/judges.log')
    fmt = logging.Formatter("[%(asctime)s |%(levelname)s]: %(message)s")
    handler.setFormatter(fmt)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def main():
    """
    Fork master process and start flask server in current process and pool of workers
    :return:
    """
    startup()
    print(f'Pid: {os.getpid()}')
    queue = multiprocessing.Queue()
    pid = os.fork()
    if pid == 0:
        app.mp_queue = queue
        atexit.register(shutdown)
        app.run(host=config.IP, port=config.PORT, debug=False)
    else:
        worker.run(queue)


if __name__ == '__main__':
    main()
