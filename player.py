"""
Contains the Player superclass and its subclasses.
"""

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
        self.filled_edges = filled
        self.filled_surrounded = []
        self.game_board = game_board

        self.color = self.game_board.get_color(self.filled_edges[0])
        self.game_board.update_filled(self.filled_edges, self.filled_surrounded)

    def play_turn(self, color_options):
        """
        Plays a turn by choosing a color, setting it, updating the list of filled cells, and sets the score.

        Parameters
        ----------
        color_options : list
            a list of the possible color options (as integers)
        """
        self.color = self.choose_color(color_options)
        self.game_board.set_color(self.color, self.filled_edges + self.filled_surrounded)
        self.game_board.update_filled(self.filled_edges, self.filled_surrounded)
        self.score = len(self.filled_edges) + len(self.filled_surrounded)

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
        np.random.shuffle(color_options)
        counts = [self.game_board.get_color_count(color, self.filled_edges.copy()) for color in color_options]

        return color_options[np.argmax(counts)]


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


class RLPlayer(Player):
    """
    A subclass of Player in which the color is pre-selected by an RL agent.
    """

    def choose_color(self, color_options):
        """
        Chooses the pre-selected color.

        Parameters
        ----------
        color_options : list
            a list containing the pre-selected color

        Returns
        -------
        int
            the integer of the pre-selected color
        """
        return color_options[0]
