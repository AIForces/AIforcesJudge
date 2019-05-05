import random
import subprocess as sp

from .exceptions import CompilationError, PresentationError


class State:

    def get_start_field(self):
        ans = [[0] * 5] * 5
        ans[0][0] = 1
        ans[-1][-1] = 2
        return ans

    def __init__(self):
        self.current_player = 0
        self.field = self.get_start_field()
        self.gameover = 0
        self.points = [0, 0]
        self.verdicts = ["OK", "OK"]

    def change_state(self, output):
        pass
        # Change state

    def get_winner(self):
        if self.points[0] > self.points[1]:
            return "Player 1"
        else:
            return "Player 2"

    def change_player(self):
        self.current_player ^= 1

    # return input for cur player
    def get_input(self):
        pass

    def player_error(self, player, error):
        self.verdicts[player] = error
        self.points[player] = -1
        self.endgame = 1


class BaseJudge:

    def __init__(self, lang1: str, source1: str, lang2: str, source2: str, timeout: float):
        self._source = [source1, source2]
        self._lang = [lang1, lang2]
        self._cmd = ['', '']
        self._results = ['OK', 'OK']
        self._winner = None
        self._timeout = timeout
        self._state = State()

    def _before_run(self):
        """
        prepare all files, compile c++ and java, get command for running fighters
        :return:

        """
        filenames = ['first', 'second']
        for player in range(2):
            try:
                self._cmd = self._compile(lang=self._lang[player], source=self._source[player], file_name=filenames[player])
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

    def run(self):
        # TODO: add memory check
        self._before_run()
        log = []

        while not self._state.endgame:
            player = sp.Popen(self._cmd[self._state.current_player], stdin=self._state.get_input(), stdout=sp.PIPE,
                              stderr=sp.DEVNULL)
            output = None
            try:
                output, _ = player.communicate(timeout=self._timeout)
            except sp.TimeoutExpired:
                self._state.player_error(self._state.current_player, "TL")
                continue

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
