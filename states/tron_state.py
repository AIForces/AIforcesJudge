from .base_state import BaseState
from exceptions import *


class State(BaseState):
    def _get_start_field(self):
        return [
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3]
        ]

    def __init__(self):
        super().__init__()
        self.field_id = 1
        self.field = self._get_start_field()
        self.size = [len(self.field), len(self.field[0])]
        self.number_of_move = 0
        self.active_power_ups = []
        self.points = [1, 1]
        self.possible_moves = ['L', 'R', 'U', 'D']
        self.delta = [
            [0, 0, -1, 1],
            [-1, 1, 0, 0]
        ]
        self.alive = [True, True]

    def find_me(self, player):
        pointer_id = 1 if player == 0 else 3
        for i, row in enumerate(self.field):
            try:
                j = row.index(pointer_id)
                return i, j
            except ValueError:
                pass

    def check_bound(self, x):
        for i, val in enumerate(x):
            if val not in range(0, self.size[i]):
                return 1
        return 0

    def check_empty(self, x):
        if self.field[x[0]][x[1]] not in [0, 6, 7, 8]:
            return 1
        else:
            return 0

    def update_alive(self):
        for player in range(2):
            my_position = self.find_me(player)
            self.alive[player] = False
            for move_id in range(4):
                next_position = [my_position[i] + self.delta[i][move_id] for i in range(2)]
                if not self.check_bound(next_position):
                    self.alive[player] |= not self.check_empty(next_position)

    def change_state(self, output):
        try:
            move = output.split()[0]
        except IndexError:
            raise PresentationError
        try:
            move_id = self.possible_moves.index(move)
        except ValueError:
            raise PresentationError

        my_position = self.find_me(self.current_player)
        next_position = [my_position[i] + self.delta[i][move_id] for i in range(2)]
        if self.check_bound(next_position):
            raise MoveError
        if self.check_empty(next_position):
            raise MoveError
        trailing_id = 2 if self.current_player == 0 else 4
        pointer_id = 1 if self.current_player == 0 else 3
        self.field[next_position[0]][next_position[1]] = pointer_id
        self.field[my_position[0]][my_position[1]] = trailing_id
        self.points[self.current_player] += 1

        self.update_alive()
        self.check_endgame()

    def check_endgame(self):
        self.game_over = self.alive == [False, False]

    def get_input(self):
        ans = ''
        if self.number_of_move < 2:
            ans += "{}\n".format(self.field_id)
        ans += "{} {}\n".format(self.size[0], self.size[1])

        cur_field = self.field
        if self.current_player == 1:
            reverse = [0, 3, 4, 1, 2, 5, 6, 7, 8]
            cur_field = [[reverse[x] for x in row] for row in self.field]
        ans += '\n'.join([' '.join(str(y) for y in x) for x in cur_field])
        ans += '\n'
        return ans

    def get_log(self):
        return {
            "field": self.field,
            "current_player": self.current_player,
            "game_over": self.game_over,
            "points": self.points,
            "verdicts": self.verdicts,
        }

    def change_player(self):
        if self.alive[self.current_player ^ 1]:
            self.current_player ^= 1
        self.number_of_move += 1
