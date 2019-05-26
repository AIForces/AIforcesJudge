import multiprocessing as mp
import subprocess
import os

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
        lang=data['lang'],
        source=data['source'],
        timeout=data['timeout'],
        challenge_id=data['challenge_id'],
        state_par=data['state_par']
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

    # python3 -m venv venv
    code = subprocess.call(['python3', '-m', 'venv', 'venv'])

    print(f"init new worker {os.getpid()}")
