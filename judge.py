import json
import subprocess as sp

import requests

import states
import config
from exceptions import *



def _get_state(game: str) -> states.BaseState:

    _module = getattr(states, f'{game}_state')
    return _module.State()


class Judge:

    def __init__(self, game: str, lang1: str, source1: str, lang2: str, source2: str, timeout: float, query_id: int):
        self._source = [source1, source2]
        self._lang = [lang1, lang2]
        self._cmd = [[], []]
        self._results = ['OK', 'OK']
        self._winner = None
        self._timeout = timeout
        self._query_id = query_id
        self._state = _get_state(game)

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
                self._state.player_error(player, "CE")

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
            source_file = f"{file_name}.cpp"
            open(source_file, 'w').write(source)

            code = sp.call(['g++', '-std=c++17', '-O2', '-o', file_name, source_file])
            if code != 0:
                raise CompilationError

            command = [f"./{file_name}"]

        elif 'python' in lang:
            source_file = f"{file_name}.py"
            open(source_file, 'w').write(source)

            command = ["python3", source_file]

        elif 'java' in lang:
            # TODO: add java support
            raise NotImplementedError

        return command

    def _send_result(self):
        # TODO: wtf where is log?
        data = {
            "query_id": self._query_id,
            "player_1_verdict": self._results[0],
            "player_2_verdict": self._results[1],
            "winner": self._winner,
            "log": self._state.field
        }
        requests.post(config.RESULT_ENDPOINT, data=json.dumps(data))

    def run(self):
        # TODO: add memory check
        self._before_run()
        log = []
        while not self._state.game_over:
            player = sp.Popen(self._cmd[self._state.current_player], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.DEVNULL)
            output = None
            try:
                output, _ = player.communicate(input=str.encode(self._state.get_input()), timeout=self._timeout)
            except sp.TimeoutExpired:
                self._state.player_error(self._state.current_player, "TL")
                continue

            print(self._state.get_input())
            print(output)

            if player.returncode != 0:
                self._state.player_error(self._state.current_player, "RE")
                continue
            try:
                self._state.change_state(output)
            except PresentationError:
                self._state.player_error(self._state.current_player, "PE")
                continue

            self._state.change_player()
            log.append(self._state)

        winner = self._state.get_winner()
        self._send_result()