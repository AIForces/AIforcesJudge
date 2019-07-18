import importlib
import os
import subprocess as sp
from copy import deepcopy
from os.path import join
from select import select

import requests
from loguru import logger

from states.base_state import *
from sandbox import Sandbox
import config
import states
from exceptions import *


NEED_REIMPORT_STATES = False


def _get_state(game: str):
    global NEED_REIMPORT_STATES
    if NEED_REIMPORT_STATES:
        importlib.reload(states)
        NEED_REIMPORT_STATES = False

    _module = getattr(states, f'{game}_state')
    return _module.State


class Judge:

    def __init__(self, game: str, lang: list, source: list, timeout: float, challenge_id: int, state_par, local=False):
        self._source = source
        self._lang = lang
        self._cmd = [[], []]
        self._timeout = timeout
        self._challenge_id = challenge_id
        self._state = _get_state(game)(state_par)
        self._log = []
        self._local = local

        self.streams_log = {
            "stdin": {
                Players.RED: [],
                Players.BLUE: [],
            },
            "stdout": {
                Players.RED: [],
                Players.BLUE: [],
            },
            "stderr": {
                Players.RED: [],
                Players.BLUE: [],
            }
        }


    def _before_run(self):
        '''
        prepare all files, compile c++ and java, get command for running fighters
        :return:

        '''
        filenames = ['first', 'second']
        for player in range(2):
            try:
                self._cmd[player] = self._compile(lang=self._lang[player],
                                                  source=self._source[player],
                                                  file_name=filenames[player])
            except CompilationError:
                player_enum = Players.RED if player == 0 else Players.BLUE
                self._state.player_error(player_enum, 'CE')

    def _compile(self, lang: str, source: str, file_name: str) -> list:
        '''
        compile program and return
        :param lang:
        :param source:
        :param file_name:
        :return:
        '''

        '''
        FROM SANYA:
        Simple check of lang (if lang == 'GNU G++ 17 7.3.0':)?
        Define ONLINE_JUDGE

        Langs:
        
        'GNU G++ 17 7.3.0'
        Are these options useful?
        g++.exe -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++11 -D__USE_MINGW_ANSI_STDIO=0 -o {filename}.exe {file}
        
        'Python 3.7.3'

        'JAVA XXX?' (CF: Java 1.8.0_162 Fsystem: Java 1.8)
        Compiling java: 'java.exe -Xmx512M -Xss64M -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US -jar %s'

        Source: https://codeforces.com/blog/entry/79
        '''
        lang = lang.lower()
        command = ''
        if 'c++' in lang:
            source_file = f'{file_name}/{file_name}.cpp'
            open(source_file, 'w').write(source)
            code = sp.call(['g++', '-std=c++17', '-O2', '-o', f'{file_name}/{file_name}', source_file])
            if code != 0:
                raise CompilationError

            command = [f'./{file_name}']

        elif 'python' in lang:
            source_file = f'{file_name}/{file_name}.py'
            open(source_file, 'w').write(source)
            command = [join(file_name, join(config.PYTHON_VENV_PATH, 'python3')), f'{file_name}.py']
            print('command is:')
            print(command)

        elif 'java' in lang:
            # TODO: add java support
            raise NotImplementedError

        return command

    def get_streams_log(self):
        log = {}
        for stream in ['stdin', 'stdout', 'stderr']:
            log[stream] = {}
            for player in Players:
                log[stream][player.value] = self.streams_log[stream][player]
        return log

    def _compose_response(self):
        return {
            'challenge_id': self._challenge_id,
            'verdicts': self._state.get_verdicts(),
            'winner': self._state.get_winner(),
            'log': self._log,
            'streams': self.get_streams_log()
        }

    def _update_status(self, stage):
        if self._local:
            return

        if config.SEND_STATUS:
            r = None
            try:
                r = requests.post(config.SUBMISSION_STATUS_ENDPOINT, json={
                    'challenge_id': self._challenge_id,
                    'stage': stage,
                    'step': self._state.number_of_move
                })
            except ConnectionError:
                logger.critical('server not available')

            if r.status_code != 200:
                logger.critical('error while updating result')

    def run(self):
        try:
            self._run()

        except Exception as e:
            self._state.player_error(self._state.current_player, 'FT')
            self._state.change_player()
            self._state.player_error(self._state.current_player, 'FT')

            logger.critical(f'FT on challenge #{self._challenge_id}')
            logger.exception(e)

        return self._compose_response()

    def _run(self):
        self._update_status(stage='Preparing')
        self._before_run()
        players = None
        if not self._state.game_over:
            players = [Sandbox.run(self._cmd[i], i) for i in range(2)]
            self._log.append(deepcopy(self._state.get_log()))
            logger.info(f'starting challenge #{self._challenge_id}')

        while not self._state.game_over:
            logger.debug(f'# {self._challenge_id} step {self._state.number_of_move}')
            self._update_status(stage='Running')

            player = players[self._state.current_player.value]
            if player.poll() is not None:
                self._state.player_error(self._state.current_player, 'RE')
                message = f'Process unexpectedly terminated.'
                for stream in ('stdin', 'stdout', 'stderr'):
                    self.streams_log[stream][player].append(message)
                continue

            current_stdin = self._state.get_input()
            print("cur_stdin")
            print(current_stdin)
            player.stdin.write(current_stdin)
            player.stdin.flush()

            pipes = select([player.stdout, player.stderr], [], [], self._timeout)[0]

            # no data to read in player.stdout
            if player.stdout not in pipes:
                logger.debug('TL')
                self._state.player_error(self._state.current_player, 'TL')
                continue

            try:
                current_stdout = os.read(player.stdout.fileno(), 1000).decode()
            except UnicodeDecodeError:
                logger.error("Can't decode user's stdout... PE")
                self._state.player_error(self._state.current_player, 'PE')
                continue

            if player.stderr in pipes:
                try:
                    current_stderr = os.read(player.stderr.fileno(), 1000).decode()
                except UnicodeDecodeError:
                    logger.warning("Can't decode user's stderr... Skipping")
                    current_stderr = ''
            else:
                logger.debug("no_stderr to read")
                current_stderr = ''

            try:
                self._state.change_state(current_stdout)
            except PresentationError:
                self._state.player_error(self._state.current_player, 'PE')
                continue
            except MoveError:
                self._state.player_error(self._state.current_player, 'ME')
                continue

            self.streams_log['stdin'][self._state.current_player].append(current_stdin)
            self.streams_log['stdout'][self._state.current_player].append(current_stdout)
            self.streams_log['stderr'][self._state.current_player].append(current_stderr)

            for stream in ('stdin', 'stdout', 'stderr'):
                self.streams_log[stream][BaseState.get_other_player(self._state.current_player)].append("[Waiting for opponent's move]")

            self._log.append(deepcopy(self._state.get_log()))
            self._state.change_player()

        self._log.append(deepcopy(self._state.get_log()))
        if players is not None:
            for player in players:
                player.kill()
                message = f'Process killed'
                for stream in ('stdin', 'stdout', 'stderr'):
                    self.streams_log[stream][self._state.current_player].append(message)
