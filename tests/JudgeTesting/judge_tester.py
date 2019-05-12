from judge import Judge

if __name__ == '__main__':
    source = open("player.cpp").read()
    jdg = Judge("tictactoe", "c++", source, "c++", source, 2.0)
    jdg.run()
    