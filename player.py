"""
Contains the Player superclass and its subclasses.
"""

import copy
import numpy as np


class Player:
    """
    A superclass to implement functions and variables for all players.
    """

    def __init__(self, filled, game_board):
        """
        Initializes the player object.

        Parameters
        ----------
        filled : list
            a list of cells that belong to the player
        game_board : FillerBoard
            the gameboard object
        """
        self.score = 1
        self.filled = filled
        self.game_board = game_board

        self.color = self.game_board.get_color(self.filled[0])
        self.game_board.update_filled(self.filled)

    def play_turn(self, color_options):
        """
        Plays a turn by choosing a color, setting it, updating the list of filled cells, and sets the score.

        Parameters
        ----------
        color_options : list
            a list of the possible color options (as integers)
        """
        self.color = self.choose_color(color_options)
        self.game_board.set_color(self.color, self.filled)
        self.game_board.update_filled(self.filled)
        self.score = len(self.filled)

    def choose_color(self, color_options):
        """
        A function to choose the color based on the options that should be implemented in subclasses.
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """
    A subclass of Player in which the user can play against the AI.
    """

    def choose_color(self, color_options):
        """
        Chooses a color using valid user input.

        Parameters
        ----------
        color_options : list
            a list of the possible color options (as integers)

        Returns
        -------
        int
            the integer of the chosen color
        """
        from filler import COLORS

        color_options_names = [(i, list(COLORS.keys())[i]) for i in color_options]
        print(f'Color options: {color_options_names}')

        while True:
            try:
                chosen_color = int(input('Choose a color by number: '))
                if chosen_color not in color_options:
                    raise ValueError

                return chosen_color
            except ValueError:
                print('Invalid input.\n')


class AIPlayer(Player):
    """
    A subclass of Player in which the colors are chosen to maximize the score.
    """

    def choose_color(self, color_options):
        """
        Chooses a color that will maximize the score using depth-first search.

        Parameters
        ----------
        color_options : list
            a list of the possible color options (as integers)

        Returns
        -------
        int
            the integer of the best color
        """
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
    """
    A subclass of Player in which the colors are chosen randomly.
    """

    def choose_color(self, color_options):
        """
        Chooses a color randomly.

        Parameters
        ----------
        color_options : list
            a list of the possible color options (as integers)

        Returns
        -------
        int
            the integer of the randomly chosen color
        """
        return np.random.choice(color_options)
