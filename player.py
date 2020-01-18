import copy
import numpy as np

from filler import COLORS


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


class HumanPlayer(Player):
    def choose_color(self, color_options):
        color_options_names = [(i, list(COLORS.keys())[i]) for i in color_options]
        print(f'Color options: {color_options_names}')
        self.game_board.graphical_output()

        while True:
            chosen_color = int(input('Choose a color by number: '))
            if chosen_color in color_options:
                return chosen_color
            else:
                print('Invalid input.')


class AIPlayer(Player):
    def choose_color(self, color_options):
        max_score = -1
        best_color = -1

        np.random.shuffle(color_options)
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
