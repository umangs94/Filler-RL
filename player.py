import copy
import numpy as np


class Player:
    def __init__(self, filled, game_board):
        self.score = 1
        self.filled = filled
        self.game_board = game_board

        self.color = self.game_board.get_color(self.filled[0])
        self.game_board.update_filled(self.filled)

    def play_turn(self, color_options):
        self.color = self.choose_color(color_options)
        self.game_board.set_color(self.color, self.filled)
        self.game_board.update_filled(self.filled)
        self.score = len(self.filled)

    def choose_color(self, color_options):
        raise NotImplementedError


class AIPlayer(Player):
    def choose_color(self, color_options):
        max_score = -1
        best_color = -1

        for color in color_options:
            simulated_game_board = copy.copy(self.game_board)
            simulated_filled = self.filled.copy()

            simulated_game_board.set_color(color, simulated_filled)
            simulated_game_board.update_filled(simulated_filled)
            simulated_score = len(simulated_filled)

            if simulated_score > max_score:
                max_score = simulated_score
                best_color = color

        return best_color


class RandomPlayer(Player):
    def choose_color(self, color_options):
        return np.random.choice(color_options)
