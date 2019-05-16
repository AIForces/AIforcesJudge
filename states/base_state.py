from abc import abstractmethod, ABC
from enum import Enum


class Players(Enum):
    RED = 0
    BLUE = 1


class BaseState(ABC):

    def __init__(self):
        self.points = {
            Players.RED: 0,
            Players.BLUE: 0
        }
        self.current_player = Players.RED
        self.game_over = False
        self.verdicts = {
            Players.RED: "OK",
            Players.BLUE: "OK"
        }

    @abstractmethod
    def change_state(self, output):
        pass

    def get_winner(self):
        if self.points[Players.RED] > self.points[Players.BLUE]:
            return 0
        elif self.points[Players.BLUE] < self.points[Players.RED]:
            return 1
        else:
            return -1

    def change_player(self):
        self.current_player = BaseState.get_other_player(self.current_player)

    @abstractmethod
    def get_input(self):
        pass

    @abstractmethod
    def get_log(self):
        pass

    def get_verdicts(self):
        return [self.verdicts[Players.RED], self.verdicts[Players.BLUE]]

    @staticmethod
    def get_other_player(player):
        return Players.BLUE if player == Players.RED else Players.RED

    def player_error(self, player, error):
        self.verdicts[player] = error
        self.points[player] = -1
        self.game_over = True
