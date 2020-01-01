languages = {
  "gcc11": {
    'name': 'GNU GCC C11',
    'compilation': 'gcc -static -fno-optimize-sibling-calls -fno-strict-aliasing -DONLINE_JUDGE -fno-asm -lm -s -Wl,'
                   '--stack=268435456 -O2 -o bin/$file.executable $file',
    'running': './bin/$file.executable'
  },
  "g++11": {
    'name': 'GNU G++11',
    'compilation': 'g++ -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++11 -o '
                   'bin/$file.executable $file',
    'running': './bin/$file.executable'
  },
  "g++14": {
    'name': 'GNU G++14',
    'compilation': 'g++ -static -DONLINE_JUDGE -lm -s -x c++ -Wl,--stack=268435456 -O2 -std=c++14 -o bin/$file.executable $file',
    'running': './bin/$file.executable'
  },
  "g++17": {
    'name': 'GNU G++17',
    'compilation': 'g++ -DONLINE_JUDGE -O2 -std=c++17 -o bin/$file sources/$file',
    'running': './bin/$file'
  },
# TODO: change to venv
  "py": {
    'name': 'Python 2.7.17',
    'compilation': 'cp $file bin/$file.executable $file',
    'running': 'python $file'
  },
  "py3": {
    'name': 'Python 3.8.1',
    'compilation': 'cp $file bin/$file.executable $file',
    'running': 'python3 $file'
  },
  "pypy": {
    'name': 'PyPy2.7 v7.3.0',
    'compilation': 'cp $file bin/$file.executable $file',
    'running': 'pypy $file'
  },
  "pypy3": {
    'name': 'PyPy3.6 v7.3.0',
    'compilation': 'cp $file bin/$file.executable $file',
    'running': 'pypy3 $file'
  },

  "java": {
    'name': 'Java SE 13.0.1',
    'compilation': 'javac -cp ".;*" $file',
    'running': 'java -Xmx512M -Xss64M -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US -jar '
               '$file '
  }
}

extensions = {
  "gcc11": "c",
  "g++11": "cpp",
  "g++14": "cpp",
  "g++17": "cpp",
  "py": "py",
  "py3": "py",
  "pypy": "py",
  "pypy3": "py",
  "java": "java"
}
