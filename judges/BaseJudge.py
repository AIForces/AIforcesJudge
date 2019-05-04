import subprocess as sp

from .exceptions import CompilationError


class BaseJudge:

    def __init__(self, lang1: str, source1: str, lang2: str, source2: str):
        self._lang1 = lang1
        self._source1 = source1
        self._lang2 = lang2
        self._source2 = source2
        self._state = None
        self._cmd1 = None
        self._cmd2 = None
        self._result1 = 'OK'
        self._result2 = 'OK'
        self._winner = None

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

    def _compile(self, lang: str, source: str, file_name: str):
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
            #TODO: add java support
            raise NotImplementedError

        return command

    def run(self):
        # TODO: add memory check
        self._before_run()
        if self._winner is None:
            fighter1 = sp.Popen
        while self._winner is None:
            pass

    def check(self):
        pass



