from .base_state import BaseState
from exceptions import *


class State(BaseState):
    def _get_start_field(self):
        w, h = 3, 3
        return [[0 for x in range(w)] for y in range(h)]

    def __init__(self):
        super().__init__()

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
                    self.game_over = 1

        for col in range(3):
            for player in range(2):
                if [row[col] for row in self.field] == [player + 1] * 3:
                    self.points[player] = 1
                    self.game_over = 1

        for player in range(2):
            if [self.field[i][i] for i in range(3)] == [player + 1] * 3:
                self.points[player] = 1
                self.game_over = 1

            if [self.field[i][2 - i] for i in range(3)] == [player + 1] * 3:
                self.points[player] = 1
                self.game_over = 1

        non_empty = sum([sum(item != 0 for item in row) for row in self.field])
        if non_empty == 0:
            self.game_over = 1

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
