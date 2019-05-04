import multiprocessing
import os

import flask

from app import app
import worker


if __name__ == '__main__':
    queue = multiprocessing.Queue()
    pid = os.fork()
    if pid != 0:
        app.mp_queue = queue
        app.run(port=3001, debug=True)
    else:
        worker.run(queue)
