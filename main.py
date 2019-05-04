import multiprocessing
import os
import shutil

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


def main():
    """
    Fork master process and start flask server in current process and pool of workers
    :return:
    """
    startup()
    queue = multiprocessing.Queue()
    pid = os.fork()
    if pid != 0:
        app.mp_queue = queue
        app.run(host=config.IP, port=config.PORT, debug=config.DEBUG)
    else:
        worker.run(queue)


if __name__ == '__main__':
    main()
