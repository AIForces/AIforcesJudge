from .base_state import *
from exceptions import *
from enum import Enum
import copy


class BoardCells(Enum):
    EMPTY = 0, '.'
    RED_PLAYER = 1, 'R'
    RED_PLAYER_DEAD = 2, 'R'
    RED_TAIL_VERTICAL = 3, 'Q'
    RED_TAIL_HORIZONTAL = 4, 'Q'
    RED_TAIL_CORNER_LU = 5, 'Q'
    RED_TAIL_CORNER_LD = 6, 'Q'
    RED_TAIL_CORNER_RU = 7, 'Q'
    RED_TAIL_CORNER_RD = 8, 'Q'
    RED_TAIL_START_L = 9, 'Q'
    RED_TAIL_START_R = 10, 'Q'
    RED_TAIL_START_U = 11, 'Q'
    RED_TAIL_START_D = 12, 'Q'
    BLUE_PLAYER = 13, 'B'
    BLUE_PLAYER_DEAD = 14, 'B'
    BLUE_TAIL_VERTICAL = 15, 'W'
    BLUE_TAIL_HORIZONTAL = 16, 'W'
    BLUE_TAIL_CORNER_LU = 17, 'W'
    BLUE_TAIL_CORNER_LD = 18, 'W'
    BLUE_TAIL_CORNER_RU = 19, 'W'
    BLUE_TAIL_CORNER_RD = 20, 'W'
    BLUE_TAIL_START_L = 21, 'W'
    BLUE_TAIL_START_R = 22, 'W'
    BLUE_TAIL_START_U = 23, 'W'
    BLUE_TAIL_START_D = 24, 'W'
    BLOCK = 25, 'X'
    COIN = 26, 'C'
    SPEED_UP = 27, 'U'
    SPEED_DOWN = 28, 'D'
    INVISIBILITY = 29, 'I'


class Move:
    def __init__(self, delta, literal):
        self.delta = delta
        self.literal = literal


class Moves(Enum):
    START = Move([0, 0], 'S')
    UP = Move([-1, 0], 'U')
    DOWN = Move([1, 0], 'D')
    LEFT = Move([0, -1], 'L')
    RIGHT = Move([0, 1], 'R')


class PowerUps(str, Enum):
    COIN = 'COIN'
    SPEED_UP = 'SPEED_UP'
    SPEED_DOWN = 'SPEED_DOWN'
    INVISIBILITY = 'INVISIBILITY'


class State(BaseState):
    @staticmethod
    def get_start_board(level):
        x = BoardCells.BLOCK
        e = BoardCells.EMPTY
        r = BoardCells.RED_PLAYER
        b = BoardCells.BLUE_PLAYER
        c = BoardCells.COIN
        u = BoardCells.SPEED_UP
        d = BoardCells.SPEED_DOWN

        if level == 1:
            w, h = 25, 25
            ans = [[e for _ in range(h)] for _ in range(w)]
            ans[0][0] = r
            ans[-1][-1] =b
        elif level == 2:
            w, h = 20, 20
            ans = [[e for _ in range(h)] for _ in range(w)]
            basic_comp = [
                [
                    [x, x],
                    [x, e]
                ],
                [
                    [x for _ in range(8)]
                ]
            ]
            blocks = []
            for comp in basic_comp:
                blocks.append(comp)
                for _ in range(3):
                    blocks.append(list(zip(*blocks[-1][::-1])))
            positions = [
                [2, 2],
                [2, 16],
                [16, 16],
                [16, 2],

                [4, 6],
                [6, 15],
                [15, 6],
                [6, 4]
            ]

            for i, pos in enumerate(positions):
                for x, row in enumerate(blocks[i]):
                    for y, val in enumerate(row):
                        ans[x + pos[0]][y + pos[1]] = val
            ans[0][0] = BoardCells.RED_PLAYER
            ans[-1][-1] = BoardCells.BLUE_PLAYER

        elif level == 3:
            half = [
                [r, e, c, c, x, c, c, c, e, x, c, e, e, c, x, e, c, c, c],
                [e, e, x, x, x, x, x, x, e, x, x, e, x, c, x, e, x, x, x],
                [e, e, x, e, e, x, c, x, e, e, x, e, x, c, x, e, e, e, c],
                [e, e, e, e, e, x, e, e, e, e, x, e, x, c, c, e, x, e, x],
                [x, x, x, e, e, x, e, e, e, x, x, e, x, x, x, e, x, e, c],
                [x, c, c, e, x, x, x, x, e, x, u, e, e, e, e, e, x, e, x],
                [x, x, x, e, e, e, e, e, e, x, e, e, e, e, e, e, x, e, e],
                [e, e, e, e, x, x, x, x, e, x, x, e, x, x, e, e, x, x, e],
                [e, x, x, e, c, x, x, e, e, e, e, e, d, x, e, e, e, e, e],
                [e, c, x, e, x, x, x, e, x, x, x, x, e, x, e, x, x, x, x]
            ]
            ans = copy.copy(half) + copy.copy(half)[-2::-1]
            ans[-1][0] = b
        else:
            raise NotImplementedError

        return ans

    @staticmethod
    def get_tail_type(player, last, cur):
        tail_mapper = {
            (Players.RED, Moves.START, Moves.UP): BoardCells.RED_TAIL_START_U,
            (Players.RED, Moves.START, Moves.DOWN): BoardCells.RED_TAIL_START_D,
            (Players.RED, Moves.START, Moves.LEFT): BoardCells.RED_TAIL_START_L,
            (Players.RED, Moves.START, Moves.RIGHT): BoardCells.RED_TAIL_START_R,
            (Players.RED, Moves.UP, Moves.UP): BoardCells.RED_TAIL_VERTICAL,
            (Players.RED, Moves.UP, Moves.LEFT): BoardCells.RED_TAIL_CORNER_LD,
            (Players.RED, Moves.UP, Moves.RIGHT): BoardCells.RED_TAIL_CORNER_RD,
            (Players.RED, Moves.DOWN, Moves.DOWN): BoardCells.RED_TAIL_VERTICAL,
            (Players.RED, Moves.DOWN, Moves.LEFT): BoardCells.RED_TAIL_CORNER_LU,
            (Players.RED, Moves.DOWN, Moves.RIGHT): BoardCells.RED_TAIL_CORNER_RU,
            (Players.RED, Moves.LEFT, Moves.UP): BoardCells.RED_TAIL_CORNER_RU,
            (Players.RED, Moves.LEFT, Moves.DOWN): BoardCells.RED_TAIL_CORNER_RD,
            (Players.RED, Moves.LEFT, Moves.LEFT): BoardCells.RED_TAIL_HORIZONTAL,
            (Players.RED, Moves.RIGHT, Moves.UP): BoardCells.RED_TAIL_CORNER_LU,
            (Players.RED, Moves.RIGHT, Moves.DOWN): BoardCells.RED_TAIL_CORNER_LD,
            (Players.RED, Moves.RIGHT, Moves.RIGHT): BoardCells.RED_TAIL_HORIZONTAL,
            (Players.BLUE, Moves.START, Moves.UP): BoardCells.BLUE_TAIL_START_U,
            (Players.BLUE, Moves.START, Moves.DOWN): BoardCells.BLUE_TAIL_START_D,
            (Players.BLUE, Moves.START, Moves.LEFT): BoardCells.BLUE_TAIL_START_L,
            (Players.BLUE, Moves.START, Moves.RIGHT): BoardCells.BLUE_TAIL_START_R,
            (Players.BLUE, Moves.UP, Moves.UP): BoardCells.BLUE_TAIL_VERTICAL,
            (Players.BLUE, Moves.UP, Moves.LEFT): BoardCells.BLUE_TAIL_CORNER_LD,
            (Players.BLUE, Moves.UP, Moves.RIGHT): BoardCells.BLUE_TAIL_CORNER_RD,
            (Players.BLUE, Moves.DOWN, Moves.DOWN): BoardCells.BLUE_TAIL_VERTICAL,
            (Players.BLUE, Moves.DOWN, Moves.LEFT): BoardCells.BLUE_TAIL_CORNER_LU,
            (Players.BLUE, Moves.DOWN, Moves.RIGHT): BoardCells.BLUE_TAIL_CORNER_RU,
            (Players.BLUE, Moves.LEFT, Moves.UP): BoardCells.BLUE_TAIL_CORNER_RU,
            (Players.BLUE, Moves.LEFT, Moves.DOWN): BoardCells.BLUE_TAIL_CORNER_RD,
            (Players.BLUE, Moves.LEFT, Moves.LEFT): BoardCells.BLUE_TAIL_HORIZONTAL,
            (Players.BLUE, Moves.RIGHT, Moves.UP): BoardCells.BLUE_TAIL_CORNER_LU,
            (Players.BLUE, Moves.RIGHT, Moves.DOWN): BoardCells.BLUE_TAIL_CORNER_LD,
            (Players.BLUE, Moves.RIGHT, Moves.RIGHT): BoardCells.BLUE_TAIL_HORIZONTAL,
        }
        return tail_mapper[player, last, cur]

    @staticmethod
    def get_move_enum(lit):
        for move in Moves:
            if move.value.literal == lit:
                return move
        raise ValueError

    def __init__(self, state_par):
        super().__init__(state_par)
        self.level = state_par["level"]
        self.board = State.get_start_board(state_par["level"])
        self.size = [len(self.board), len(self.board[0])]
        self.number_of_move = 0
        self.power_ups = {
            Players.RED: {
                PowerUps.SPEED_DOWN: 0,
                PowerUps.SPEED_UP: 0,
                PowerUps.INVISIBILITY: 0,
            },
            Players.BLUE: {
                PowerUps.SPEED_DOWN: 0,
                PowerUps.SPEED_UP: 0,
                PowerUps.INVISIBILITY: 0,
            }
        }
        self.points = {
            Players.RED: 1,
            Players.BLUE: 1
        }
        self.alive = {
            Players.RED: True,
            Players.BLUE: True
        }
        self.last_move = {
            Players.RED: Moves.START,
            Players.BLUE: Moves.START
        }

        self.predicted_runs = {
            Players.RED: 1,
            Players.BLUE: 1
        }

        self.current_runs = {
            Players.RED: 0,
            Players.BLUE: 0
        }

    def find_me(self, player):
        player_cell = BoardCells.RED_PLAYER if player == Players.RED else BoardCells.BLUE_PLAYER
        for i, row in enumerate(self.board):
            try:
                j = row.index(player_cell)
                return i, j
            except ValueError:
                pass

    def check_bound(self, x):
        for i, val in enumerate(x):
            if val not in range(0, self.size[i]):
                return 1
        return 0

    def check_empty(self, x):
        if self.board[x[0]][x[1]] not in [BoardCells.EMPTY, BoardCells.COIN, BoardCells.SPEED_UP, BoardCells.SPEED_DOWN, BoardCells.INVISIBILITY]:
            return 1
        else:
            return 0

    def update_alive(self):
        for player in Players:
            my_position = self.find_me(player)
            self.alive[player] = False
            for move_enum in Moves:
                if move_enum == Moves.START:
                    continue
                move = move_enum.value
                next_position = [my_position[i] + move.delta[i] for i in range(2)]
                if not self.check_bound(next_position):
                    if not self.check_empty(next_position):
                        self.alive[player] = True
            if not self.alive[player]:
                self.predicted_runs[player] = self.current_runs[player] + int(self.current_player == player)

    def decrease_powerups(self):
        for player, data in self.power_ups.items():
            for pw, val in data.items():
                if self.power_ups[player][pw] > 0:
                    self.power_ups[player][pw] -= 1

    def change_state(self, output):
        self.decrease_powerups()

        try:
            move_lit = output.split()[0]
        except IndexError:
            raise PresentationError
        try:
            move_enum = State.get_move_enum(move_lit)
            move = move_enum.value
        except ValueError:
            raise PresentationError
        
        my_position = self.find_me(self.current_player)
        next_position = [my_position[i] + move.delta[i] for i in range(2)]

        if self.check_bound(next_position):
            raise MoveError
        if self.check_empty(next_position):
            raise MoveError

        tail_cell = State.get_tail_type(self.current_player, self.last_move[self.current_player], move_enum)
        pointer_cell = BoardCells.RED_PLAYER if self.current_player == Players.RED else BoardCells.BLUE_PLAYER
        self.last_move[self.current_player] = move_enum

        if self.board[next_position[0]][next_position[1]] == BoardCells.COIN:
            self.points[self.current_player] += 5

        if self.board[next_position[0]][next_position[1]] == BoardCells.INVISIBILITY:
            self.power_ups[self.current_player][PowerUps.INVISIBILITY] = 5

        if self.board[next_position[0]][next_position[1]] == BoardCells.SPEED_UP:
            self.power_ups[self.current_player][PowerUps.SPEED_UP] = 20

        if self.board[next_position[0]][next_position[1]] == BoardCells.SPEED_DOWN:
            self.power_ups[self.current_player][PowerUps.SPEED_DOWN] = 20

        self.board[next_position[0]][next_position[1]] = pointer_cell
        self.board[my_position[0]][my_position[1]] = tail_cell
        self.points[self.current_player] += 1

        self.update_alive()
        self.check_endgame()

    def check_endgame(self):
        self.game_over = self.alive == {
            Players.RED: False,
            Players.BLUE: False
        }

    def get_input(self):
        ans = ''
        if self.number_of_move < 2:
            ans += "{}\n".format(self.current_player.name)
            ans += "{}\n".format(self.level)
            ans += "{} {}\n".format(self.size[0], self.size[1])
        cur_board = [[j.value[1] for j in i] for i in self.board]

        ans += '\n'.join([' '.join(str(y) for y in x) for x in cur_board])
        ans += '\n'
        return ans

    def get_log(self):
        board_log = [[j.value[0] for j in i] for i in self.board]
        points_log = [self.points[player] for player in Players]
        powerups_log = [self.power_ups[player] for player in Players]
        return {
            "board": board_log,
            "current_player": self.current_player.value,
            "power_ups": powerups_log,
            "game_over": self.game_over,
            "points": points_log,
        }

    def recalc_runs(self):
        speed = {}
        for player in Players:
            speed[player] = int(self.power_ups[player][PowerUps.SPEED_UP] > 0) - int(self.power_ups[player][PowerUps.SPEED_DOWN] > 0)
        delta = speed[Players.RED] - speed[Players.BLUE]
        mapper = {
            -2: {
                Players.RED: 1,
                Players.BLUE: 4
            },
            -1: {
                Players.RED: 1,
                Players.BLUE: 2
            },
            0: {
                Players.RED: 1,
                Players.BLUE: 1
            },
            1: {
                Players.RED: 2,
                Players.BLUE: 1
            },
            2: {
                Players.RED: 4,
                Players.BLUE: 1
            }
        }
        result = mapper[delta]
        for player in Players:
            if not self.alive[player]:
                result[player] = 0

        self.current_runs = {
                Players.RED: 0,
                Players.BLUE: 0
            }
        self.predicted_runs = result

    def change_player(self):
        self.current_runs[self.current_player] += 1
        if self.current_runs[self.current_player] >= self.predicted_runs[self.current_player]:
            self.current_player = State.get_other_player(self.current_player)
        if self.current_runs == self.predicted_runs:
            self.recalc_runs()
        if self.current_runs[self.current_player] >= self.predicted_runs[self.current_player]:
            self.current_player = State.get_other_player(self.current_player)
        self.number_of_move += 1
