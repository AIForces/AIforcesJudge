import random
import subprocess as sp

# from exceptions import *

# WIll be deleted
class CompilationError(Exception):
    pass


class PresentationError(Exception):
    pass


class MoveError(Exception):
    pass


class State:
    def get_start_field(self):
        w, h = 3, 3
        return [[0 for x in range(w)] for y in range(h)]

    def __init__(self):
        self.current_player = 0
        self.field = self.get_start_field()
        self.gameover = 0
        self.points = [0, 0]
        self.verdicts = ["OK", "OK"]

    def change_state(self, output):
        try:
            x, y = [int(x) for x in output.split()]
        except IndexError:
            raise PresentationError
        rng = range(0, 3)
        if x not in rng or y not in rng:
            raise PresentationError
        if self.field[x][y] != 0:
            raise MoveError
        self.field[x][y] = self.current_player + 1

        for row in range(3):
            for player in range(2):
                if self.field[row] == [player + 1] * 3:
                    self.points[player] = 1
                    self.gameover = 1

        for col in range(3):
            for player in range(2):
                if [row[col] for row in self.field] == [player + 1] * 3:
                    self.points[player] = 1
                    self.gameover = 1

        for player in range(2):
            if [self.field[i][i] for i in range(3)] == [player + 1] * 3:
                self.points[player] = 1
                self.gameover = 1

            if [self.field[i][2 - i] for i in range(3)] == [player + 1] * 3:
                self.points[player] = 1
                self.gameover = 1

        non_empty = sum([sum(item != 0 for item in row) for row in self.field])
        if non_empty == 0:
            self.gameover = 1

    def get_winner(self):
        if self.points[0] > self.points[1]:
            return "Player 1"
        else:
            return "Player 2"

    def change_player(self):
        self.current_player ^= 1

    def get_input(self):
        if self.current_player == 0:
            ans = self.field
        else:
            ans = [[0 for x in range(3)] for y in range(3)]
            rev = [0, 2, 1]
            for i in range(3):
                for j in range(3):
                    ans[i][j] = rev[self.field[i][j]]
        return '\n'.join([' '.join(str(y) for y in x) for x in ans])

    def player_error(self, player, error):
        self.verdicts[player] = error
        self.points[player] = -1
        self.gameover = 1


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
                self._cmd[player] = self._compile(lang=self._lang[player], source=self._source[player], file_name=filenames[player])
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
        while not self._state.gameover:
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
