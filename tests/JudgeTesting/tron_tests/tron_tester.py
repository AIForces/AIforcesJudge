from judge import Judge

if __name__ == '__main__':
    source = open("player.cpp").read()
    jdg = Judge("tron", "c++", source, "c++", source, 0.5, 0)
    jdg.run()
