class CompilationError(Exception):
    pass


class PresentationError(Exception):
    pass


class State:
    def get_start_field(self):
        w, h = 3, 3
        return [[0 for x in range(w)] for y in range(h)]

    def __init__(self):
        self.current_player = 0
        self.field = self.get_start_field()
        self.gameover = 0
        self.points = [0, 0]
        self.verdicts = ["OK", "OK"]

    def change_state(self, output):
        try:
            x, y = [int(x) for x in output.split()]
        except IndexError:
            raise PresentationError
        rng = range(0, 3)
        if x not in rng or y not in rng:
            raise PresentationError
        if self.field[x][y] != 0:
            raise PresentationError
        self.field[x][y] = self.current_player + 1

        for row in range(3):
            for player in range(2):
                if self.field[row] == [player + 1] * 3:
                    self.points[player] = 1
                    self.gameover = 1

        for col in range(3):
            for player in range(2):
                if [row[col] for row in self.field] == [player + 1] * 3:
                    self.points[player] = 1
                    self.gameover = 1

        for player in range(2):
            if [self.field[i][i] for i in range(3)] == [player + 1] * 3:
                self.points[player] = 1
                self.gameover = 1

            if [self.field[i][2 - i] for i in range(3)] == [player + 1] * 3:
                self.points[player] = 1
                self.gameover = 1

    def get_winner(self):
        if self.points[0] > self.points[1]:
            return "Player 1"
        else:
            return "Player 2"

    def change_player(self):
        self.current_player ^= 1

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

    def player_error(self, player, error):
        self.verdicts[player] = error
        self.points[player] = -1
        self.gameover = 1

