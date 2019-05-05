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
        self._player_num = 1

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

    def run(self):
        # TODO: add memory check
        self._before_run()

        # FROM SANYA
        # TODO: replace with player_num = 0
        # FROM SANYA
        # while self.gameover is False?
        # Use points => determine winner after the while loop.
        # Error => Points = -1
        while self._winner is None:
            if self._player_num == 0:
                cmd = self._cmd1
            else:
                cmd = self._cmd2

            # FROM SANYA
            # self._state is not initialized.
            # State is a py class, which can be converted to string.
            # stdin = str(self._state)?
            player = sp.Popen(cmd, stdin=open('state.txt'), stdout=sp.PIPE, stderr=sp.DEVNULL)
            output = None
            try:
                output, _ = player.communicate(timeout=self._timeout)
            except sp.TimeoutExpired:
                if self._player_num == 0:
                    self._set_result(1, 'TL')
                else:
                    self._set_result(2, 'TL')

            # Check RE
            if player.returncode != 0:
                if self._player_num == 0:
                    self._set_result(1, 'RE')
                else:
                    self._set_result(2, 'RE')

            try:
                # From Sanya.
                # Check for endgame here?
                self._change_state(output)
            # PE
            except PresentationError:
                if self._player_num == 0:
                    self._set_result(1, 'PE')
                else:
                    self._set_result(2, 'PE')

            # change next player
        # From Sanya
        # if points[0] > points[1]
            # self.winner = 1
        # else
            # self.winner = 2

    def _set_result(self, num, res):
        if res == 'OK':
            self._winner = num
            # FROM SANYA
            # WTF?
            if num == 1:
                self._result1 = 'OK'
        else:
            if num == 1:
                self._winner = 2
                self._result1 = res
            else:
                self._winner = 1
                self._result2 = res

    def _change_player(self):
        pass

    def _change_state(self, step):
        pass



