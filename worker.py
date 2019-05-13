import os
import multiprocessing as mp


def run(queue: mp.Queue):
    pool = mp.Pool(initializer=init_process)
    while True:
        data = queue.get()
        send_data(Judge(data).run())
        pool.apply_async(run_fight, data, callback=callback)


def run_fight(data):
    pass


def callback(res):
    pass


def init_process():
    path = f'tmp/{os.getpid()}'
    os.mkdir(path)
    os.chdir(path)
