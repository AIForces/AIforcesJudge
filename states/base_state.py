from abc import abstractmethod, ABC


class BaseState(ABC):
    @abstractmethod
    def _get_start_field(self):
        pass

    def __init__(self):
        self.current_player = 0
        self.field = self._get_start_field()
        self.game_over = False
        self.points = [0, 0]
        self.verdicts = ["OK", "OK"]

    @abstractmethod
    def change_state(self, output):
        pass

    def get_winner(self):
        if self.points[0] > self.points[1]:
            return "Player 1"
        else:
            return "Player 2"

    def change_player(self):
        self.current_player ^= 1

    @abstractmethod
    def get_input(self):
        pass

    @abstractmethod
    def get_log(self):
        pass

    def player_error(self, player, error):
        self.verdicts[player] = error
        self.points[player] = -1
        self.game_over = True
