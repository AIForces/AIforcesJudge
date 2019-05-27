import atexit
import multiprocessing
import logging
import os
import shutil
import sys

from flask.logging import default_handler
from loguru import logger

from app import app
import worker
import config
from sandbox import Sandbox


def startup():
    """
    Create working directory for workers
    :return:
    """

    # TODO: move to configure file
    if os.path.exists('tmp'):
        shutil.rmtree('tmp')

    os.mkdir('tmp')
    Sandbox.generate_profile()

    if not os.path.exists('logs'):
        os.mkdir('logs')


def shutdown():
    logger.info('at exit')
    app.mp_queue.put('die')


def setup_logger():

    logger.remove(0)
    level = 'DEBUG' if config.DEBUG else 'INFO'
    logger.add(sys.stdout, level=level, enqueue=True)

    # remove flask default log handler
    app.logger.removeHandler(default_handler)

    # class for intercept flask logs
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            logger.debug(record)
            # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelno, record.getMessage())

    app.logger.addHandler(InterceptHandler())


def main():
    """
    Fork master process and start flask server in current process and pool of workers
    :return:
    """
    startup()
    setup_logger()
    logger.info(f'forking...')
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
