from BaseJudge import *

if __name__ == '__main__':
    source = open("player.cpp").read()
    jdg = BaseJudge("c++", source, "c++", source, 2.0)
    jdg.run()
    