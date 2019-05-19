import os
import multiprocessing as mp
from pprint import pprint

from judge import Judge


def run(queue: mp.Queue):
    logger = mp.get_logger()
    pool = mp.Pool(initializer=init_process)
    print("Starting process poll...")
    while True:
        data = queue.get()
        if isinstance(data, str) and data == 'die':
            logger.info('time to go out with a bang!')
            return
        print(type(data))
        pool.apply_async(run_fight, (data, ), callback=res_callback, error_callback=err_callback)


def run_fight(data, *args, **kwargs):

    # TODO: timeout from request
    j = Judge(
        game=data['game'],
        lang1=data['lang1'],
        source1=data['source1'],
        lang2=data['lang2'],
        source2=data['source2'],
        timeout=0.2,
        challenge_id=data['challenge_id']
    )

    j.run()


def err_callback(exc):
    print(f'ERROR at Judge \n{exc}')
    # TODO: implement errors check
    pass


def res_callback(res):
    """
    it states here just for fun
    :param res: must be None
    :return:
    """
    pass


def init_process():
    path = f'tmp/{os.getpid()}'
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)
    print(f"init new worker {os.getpid()}")
