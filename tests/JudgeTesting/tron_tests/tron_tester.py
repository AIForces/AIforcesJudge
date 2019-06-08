from judge import Judge


def test_tron(source, lang):
    j = Judge("tron", lang, source, 0.5, 0, {"level": 3}, local=True)
    j.run()


if __name__ == '__main__':
    cpp_source = open("player.cpp").read()
    py_source = open("player.py").read()
    test_tron([cpp_source, py_source], ["c++", "python"])
