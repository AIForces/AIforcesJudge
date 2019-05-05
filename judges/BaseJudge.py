import random
import subprocess as sp

from .exceptions import CompilationError, PresentationError


class BaseJudge:

    def __init__(self, lang1: str, source1: str, lang2: str, source2: str, timeout: float):
        self._lang1 = lang1
        self._source1 = source1
        self._lang2 = lang2
        self._source2 = source2
        self._cmd1 = None
        self._cmd2 = None
        self._result1 = 'OK'
        self._result2 = 'OK'
        self._winner = None
        self._timeout = timeout

    def _before_run(self):
        """
        prepare all files, compile c++ and java, get command for running fighters
        :return:
        """
        try:
            self._cmd1 = self._compile(lang=self._lang1, source=self._source1, file_name='first')
        except CompilationError:
            self._result1 = 'CE'
            self._winner = 2

        try:
            self._cmd2 = self._compile(lang=self._lang2, source=self._source2, file_name='second')
        except CompilationError:
            self._result2 = 'CE'
            self._winner = 1

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
            # From Sanya
            # Is it closed properly?
            open(source_file, 'w').write(source)

            command = ["python3", source_file]

        elif 'java' in lang:
            # TODO: add java support
            raise NotImplementedError

        return command

    class State:
        def get_start_field():
            ans = [[0] * 5] * 5
            ans[0][0] = 1
            ans[-1][-1] = 2
            return ans

        def __init__(self):
            self.current_player = 0
            self.field = get_start_field()
            self.gameover = 0
            self.points = [0, 0]
            self.verdicts = ["OK", "OK"]

        def change_state(self, output):
            if self.endgame == True:
                return
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

        def player_error(self, error):
            self.verdicts[self.current_player] = error
            self.points[self.current_player] = -1
            self.endgame = 1


    def run(self):
        # TODO: add memory check
        self._before_run()

        log = []
        mystate = State()

        while mystate.endgame == False:
            cur_cmd = cmd[mystate().current_player]
            player = sp.Popen(cur_cmd, stdin=self.mystate.get_input(), stdout=sp.PIPE, stderr=sp.DEVNULL)
            output = None
            try:
                output, _ = player.communicate(timeout=self._timeout)
            except sp.TimeoutExpired:
                mystate.player_error("TL")
            
            if player.returncode != 0:
                mystate.player_error("RE")

            try:
                mystate.change_state(output)
            except PresentationError:
                mystate.player_error("PE")

            mystate.change_player()
            log.append(mystate)

        winner = mystate.get_winner()
