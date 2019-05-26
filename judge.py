import subprocess as sp
from copy import deepcopy
from os.path import join
from select import select

from loguru import logger

from states.base_state import *
from sandbox import Sandbox
import config
import states
from exceptions import *


def _get_state(game: str):
    _module = getattr(states, f'{game}_state')
    return _module.State


class Judge:

    def __init__(self, game: str, lang: list, source: list, timeout: float, challenge_id: int, state_par):
        self._source = source
        self._lang = lang
        self._cmd = [[], []]
        self._timeout = timeout
        self._challenge_id = challenge_id
        self._state = _get_state(game)(state_par)
        self._log = []

    def _before_run(self):
        """
        prepare all files, compile c++ and java, get command for running fighters
        :return:

        """
        filenames = ['first', 'second']
        for player in range(2):
            try:
                self._cmd[player] = self._compile(lang=self._lang[player],
                                                  source=self._source[player],
                                                  file_name=filenames[player])
            except CompilationError:
                player_enum = Players.RED if player == 0 else Players.BLUE
                self._state.player_error(player_enum, "CE")

    def _compile(self, lang: str, source: str, file_name: str) -> list:
        """
        compile program and return
        :param lang:
        :param source:
        :param file_name:
        :return:
        """

        """
        FROM SANYA:
        Simple check of lang (if lang == "GNU G++ 17 7.3.0":)?
        Define ONLINE_JUDGE

        Langs:
        
        "GNU G++ 17 7.3.0"
        Are these options useful?
        g++.exe -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++11 -D__USE_MINGW_ANSI_STDIO=0 -o {filename}.exe {file}
        
        "Python 3.7.3"

        "JAVA XXX?" (CF: Java 1.8.0_162 Fsystem: Java 1.8)
        Compiling java: "java.exe -Xmx512M -Xss64M -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US -jar %s"

        Source: https://codeforces.com/blog/entry/79
        """
        lang = lang.lower()
        command = ""
        if 'c++' in lang:
            source_file = f"{file_name}/{file_name}.cpp"
            open(source_file, 'w').write(source)
            code = sp.call(['g++', '-std=c++17', '-O2', '-o', f'{file_name}/{file_name}', source_file])
            if code != 0:
                raise CompilationError

            command = [f"./{file_name}"]

        elif 'python' in lang:
            source_file = f"{file_name}/{file_name}.py"
            open(source_file, 'w').write(source)
            command = [join(file_name, join(config.PYTHON_VENV_PATH, 'python3')), f"{file_name}.py"]

        elif 'java' in lang:
            # TODO: add java support
            raise NotImplementedError

        return command

    def _compose_response(self):
        return {
            "challenge_id": self._challenge_id,
            "verdicts": self._state.get_verdicts(),
            "winner": self._state.get_winner(),
            "log": self._log
        }

    def run(self):
        # TODO: add memory check
        self._before_run()

        if not self._state.game_over:
            players = [Sandbox.run(self._cmd[i], i) for i in range(2)]
            self._log.append(deepcopy(self._state.get_log()))
            logger.info(f"starting challenge #{self._challenge_id}")
        while not self._state.game_over:
            logger.debug(f'# {self._challenge_id} step {self._state.number_of_move}')
            player = players[self._state.current_player.value]
            if player.poll() is not None:
                self._state.player_error(self._state.current_player.value, "RE")
                continue

            player.stdin.write(self._state.get_input())
            # Investigate shit. WTF newline?
            player.stdin.flush()

            # no data to read in player.stdout
            if len(select([player.stdout], [], [], self._timeout)[0]) == 0:
                logger.debug('TL')
                self._state.player_error(self._state.current_player, "TL")
                continue

            output = player.stdout.readline()
            try:
                try:
                    self._state.change_state(output)
                except PresentationError:
                    self._state.player_error(self._state.current_player, "PE")
                    continue
            except MoveError:
                self._state.player_error(self._state.current_player, "ME")
                continue

            self._log.append(deepcopy(self._state.get_log()))
            self._state.change_player()

        self._log.append(deepcopy(self._state.get_log()))
        return self._compose_response()
