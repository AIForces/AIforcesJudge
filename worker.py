import multiprocessing as mp
import subprocess as sp
import shutil
import subprocess
import requests
import config
import os
from os.path import join
import json
from requests.adapters import HTTPAdapter
from loguru import logger
from languages import extensions
from builder import build


def run(queue: mp.Queue):
    pool = mp.Pool(initializer=init_process)
    logger.info("Starting process poll...")
    while True:
        data = queue.get()
        # command task from flask
        if isinstance(data, str):

            if data == 'DIE':
                logger.info('time to go out with a bang!')
                return
            continue

        pool.apply_async(run_fight, (data,), callback=res_callback, error_callback=err_callback)


def send_as_json(invocation_id, session, file_name):
    with open(file_name) as file:
        response = session.post(config.INVOCATION_RESULT_ENDPOINT, json=json.load(file))
    if response.status_code == 200:
        logger.success(f'ID: {invocation_id}. {file_name} was sent successfully pid:{os.getpid()}')
    else:
        logger.critical(f'ID: {invocation_id}. {file_name} could not have been sent.')


def send_as_file(invocation_id, session, file_name):
    with open(file_name) as file:
        response = session.post(config.INVOCATION_RESULT_ENDPOINT, files={
            file_name: file
        })
    if response.status_code == 200:
        logger.success(f'ID: {invocation_id}. {file_name} was sent successfully pid:{os.getpid()}')
    else:
        logger.critical(f'ID: {invocation_id}. {file_name} could not have been sent.')


@logger.catch
def run_fight(data, *args, **kwargs):
    _run_fight(data['problem'], data['solutions'], data['tests'])
    session = requests.session()
    session.mount(config.RAILS_HOST, HTTPAdapter(max_retries=10))
    send_as_json(data['invocation_id'], session, 'logs/result.json')
    send_as_file(data['invocation_id'], session, 'logs/checker.log')
    send_as_file(data['invocation_id'], session, 'logs/game.json')
    send_as_file(data['invocation_id'], session, 'logs/streams.json')


def _run_fight(problem, solutions, tests):
    calls = []
    files = []
    for id, solution in enumerate(solutions):
        filename = f"solution_{id}.{extensions[solution['lang']]}"
        filepath = f'sources/{filename}'
        with open(filepath, "w") as sol:
            sol.write(solution['source'])
        calls.append(build(filename, filepath, solution['lang']))
        files.append('')
    problem_folder = os.path.join(config.PROBLEM_FOLDER, problem)
    problem_config = None
    with open(os.path.join(problem_folder, 'config/problem.json')) as file:
        problem_config = json.load(file)
    test_files = [f'{problem_folder}/tests/{x["filename"]}' for x in
                  filter(lambda x: x['id'] in tests, problem_config['tests'])]
    for file in test_files:
        return_code = sp.call(["bash", os.path.join(problem_folder, "scripts/check.sh"), '--players_cmd'] + calls +
                              ['--players_file'] + files + ['--test_file'] + [file])
        if return_code != 0:
            logger.critical(f'Checker failed with exit code {return_code}.')


def err_callback(exc):
    logger.warning(f'ERROR at Judge \n{exc}')
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
    my_wd = f'tmp/{os.getpid()}'
    if os.path.exists(my_wd):
        shutil.rmtree(my_wd)
    os.mkdir(my_wd)
    os.chdir(my_wd)

    os.mkdir('sources')
    os.mkdir('bin')
    os.mkdir('logs')

    code = subprocess.call(['python3', '-m', 'venv', 'py3_venv'])
    if code != 0:
        logger.critical(f"Error while creating python3 venv {os.getpid()}")
        exit(1)

    code = subprocess.call(['python', '-m', 'venv', 'py2_venv'])
    if code != 0:
        logger.critical(f"Error while creating python venv {os.getpid()}")
        exit(1)
    logger.success(f"init new worker {os.getpid()}")

    # code = subprocess.call(['pypy', '-m', 'venv', 'pypy2_venv'])
    # if code != 0:
    #     logger.critical(f"Error while creating pypy2 venv {os.getpid()}")
    #     exit(1)
    #
    # code = subprocess.call(['pypy3', '-m', 'venv', 'pypy3_venv'])
    # if code != 0:
    #     logger.critical(f"Error while creating pypy3 venv {os.getpid()}")
    #     exit(1)

    logger.success(f"init new worker {os.getpid()}")

