"""
Contains the FillerGame and FillerBoard classes.
"""

import numpy as np
import matplotlib.pyplot as plt

import player

COLORS = {'red': [255, 0, 0],  # red
          'orange': [255, 128, 0],  # orange
          'yellow': [255, 255, 0],  # yellow
          'green': [0, 255, 0],  # green
          'blue': [0, 0, 255],  # blue
          'purple': [127, 0, 255],  # purple
          'pink': [255, 0, 255],  # pink
          'grey': [128, 128, 128]}  # grey


class FillerGame:
    """
    Implements the game-playing functions.
    """

    def __init__(self, number_of_colors, height, width, automated):
        self.number_of_colors = number_of_colors
        self.number_of_cells = height * width
        self.color_options = np.arange(number_of_colors)
        self.game_board = FillerBoard(number_of_colors, height, width)
        self.automated = automated

        player_1_starting_cell = (height - 1, 0)
        if self.automated:
            self.player_1 = player.AIPlayer([player_1_starting_cell], self.game_board)
        else:
            self.player_1 = player.HumanPlayer([player_1_starting_cell], self.game_board)

        player_2_starting_cell = (0, width - 1)
        self.player_2 = player.AIPlayer([player_2_starting_cell], self.game_board)

    def get_color_options(self):
        """
        Returns the possible color options that can be played.

        Returns
        -------
        list
            a list of the possible color options (as integers)
        """
        mask = (self.color_options != self.player_1.color) & (self.color_options != self.player_2.color)
        return self.color_options[mask]

    def check_for_end_of_game(self):
        """
        Checks if the game is over.
        The game is over if the players' scores are greater than the number of cells 
        or if one of the players has a score greater than half the number of cells.

        Returns
        -------
        bool
            [description]
        """
        return (self.player_1.score + self.player_2.score > self.number_of_cells) | \
            (self.player_1.score > self.number_of_cells / 2) | \
            (self.player_2.score > self.number_of_cells / 2)

    def play_single_turn(self):
        """
        Completes a single turn by showing the gameboard, playing each of the players' turns, and printing the result.
        """
        self.game_board.graphical_output()
        self.player_1.play_turn(self.get_color_options())
        self.player_2.play_turn(self.get_color_options())

        print(f"player 1 played {self.player_1.color}:  {self.player_1.score}")
        print(f"player 2 played {self.player_2.color}:  {self.player_2.score}")
        print()

    def play_game(self):
        """
        Completes the entire game by playing turns until the game is over and then prints the result.
        """
        while not self.check_for_end_of_game():
            self.play_single_turn()
            if self.automated:
                input('Press any key to continue.')

        if self.player_1.score > self.player_2.score:
            print("player 1 wins!" if self.automated else "you win!")
        elif self.player_2.score > self.player_1.score:
            print("player 2 wins!" if self.automated else "you lose!")
        else:
            print("it was a tie!")
        self.game_board.graphical_output(block=True)


class FillerBoard:
    """
    Implements the functions of the gameboard, which is implemented as a 2D numpy array.
    """

    def __init__(self, number_of_colors, height, width):
        self.height = height
        self.width = width
        self.number_of_colors = number_of_colors

        plt.figure('Filler')
        plt.ion()
        plt.axis('off')

        self.board = np.random.randint(0, number_of_colors, (height, width))

    def text_output(self):
        """
        Outputs the gameboard as text.
        """
        print(self.board)
        print()

    def graphical_output(self, block=False):
        """
        Outputs the gameboard in a MatPlotLib window that is updated everytime this function is called.
        The 2D numpy array is converted to colors using the COLORS dictionary and then repeated to create an image.

        Parameters
        ----------
        block : bool, optional
            determines whether the MatPlotLib figure blocks code execution, by default False
        """
        masks = [np.where(self.board == i, True, False) for i in range(self.number_of_colors)]
        output = np.zeros((self.height, self.width, 3), dtype=np.int)
        for mask, color in zip(masks, list(COLORS.values())[:self.number_of_colors]):
            output[mask] = color

        output = np.repeat(np.repeat(output, 10, axis=0), 10, axis=1)
        plt.imsave('image.png', output)

        plt.imshow(output)
        plt.show(block)

    def get_color(self, coord):
        """
        Gets the color at the specified coordinates on the gameboard.

        Parameters
        ----------
        coord : tuple
            the coordinates in (y, x) form

        Returns
        -------
        int
            the color at the specified coordinates (as an integer)
        """
        return self.board[coord[0], coord[1]]

    def set_color(self, color, filled):
        """
        Sets the color at the specified cells on the gameboard.

        Parameters
        ----------
        color : int
            the color to set at the specified cells
        filled : list
            a list of cells that belong to the player
        """
        for cell in filled:
            self.board[cell[0], cell[1]] = color

    def update_filled(self, filled):
        """
        Updates the list of cells that belong to the player.

        Parameters
        ----------
        filled : list
            a list of cells that belong to the player
        """
        for cell in filled:
            coord_x = cell[1]
            coord_y = cell[0]
            cell_value = self.get_color(cell)

            # up
            if coord_y - 1 >= 0:
                new_cell = (coord_y-1, coord_x)
                cell_up_value = self.get_color(new_cell)
                if cell_value == cell_up_value and new_cell not in filled:
                    filled.append(new_cell)

            # down
            if coord_y + 1 < self.height:
                new_cell = (coord_y+1, coord_x)
                cell_down_value = self.get_color(new_cell)
                if cell_value == cell_down_value and new_cell not in filled:
                    filled.append(new_cell)

            # left
            if coord_x - 1 >= 0:
                new_cell = (coord_y, coord_x-1)
                cell_left_value = self.get_color(new_cell)
                if cell_value == cell_left_value and new_cell not in filled:
                    filled.append(new_cell)

            # right
            if coord_x + 1 < self.width:
                new_cell = (coord_y, coord_x+1)
                cell_right_value = self.get_color(new_cell)
                if cell_value == cell_right_value and new_cell not in filled:
                    filled.append(new_cell)
