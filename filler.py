"""
Contains the FillerGame and FillerBoard classes.
"""

import numpy as np
import matplotlib.pyplot as plt

import player

COLORS = {'red': [255, 0, 0],  # 0
          'orange': [255, 128, 0],  # 1
          'yellow': [255, 255, 0],  # 2
          'green': [0, 255, 0],  # 3
          'blue': [0, 0, 255],  # 4
          'purple': [127, 0, 255],  # 5
          'pink': [255, 0, 255],  # 6
          'grey': [128, 128, 128]}  # 7


class FillerEnv:
    """
    Implements the RL environment for the Filler game.
    """

    def __init__(self, number_of_colors, height, width):
        self.game = None
        self.number_of_colors = number_of_colors
        self.height = height
        self.width = width

    def reset(self, save_images_suffix=False):
        """
        Resets the enviroment.

        Parameters
        ----------
        save_images_suffix : bool
            the integer for the color to play
        image_suffix : str, optional
            filename suffix for the image (which is saved if not False), by default False

        Returns
        -------
        np.ndarray
            the gameboard in numpy format with shape (height, width)
        """
        self.game = FillerGame(number_of_colors=self.number_of_colors, height=self.height,
                               width=self.width, r_l=True, save_images_suffix=save_images_suffix)
        return self.game.game_board.get_board()

    def step(self, action):
        """
        Performs the specified action in the environment and returns the observation, \
            reward, and if the game is over.

        Parameters
        ----------
        action : int
            the integer for the color to play

        Returns
        -------
        np.ndarray, int, bool
            the gameboard in numpy format with shape (height, width), reward, \
                and if the game is over
        """
        self.game.play_single_turn(action)
        next_obs = self.game.game_board.get_board()
        diff = self.game.player_1.score - self.game.player_2.score
        reward = np.sign(diff) * diff ** 2 - self.game.turn_count ** 2
        done = self.game.check_for_end_of_game() or self.game.turn_count > 50

        if done:
            if self.game.player_1.score > self.game.player_2.score:
                reward += 100
            elif self.game.player_2.score > self.game.player_1.score:
                reward -= 100

            if self.game.save_images_suffix:
                image_suffix = f'{self.game.save_images_suffix}_{self.game.turn_count+1}'
                self.game.game_board.graphical_output(save=True, display=False, image_suffix=image_suffix)

        return next_obs, reward, done


class FillerGame:
    """
    Implements the game-playing functions.
    """

    def __init__(self, number_of_colors, height, width, automated=False, r_l=False, save_images_suffix=False):
        self.number_of_cells = height * width
        self.all_colors = np.arange(number_of_colors)
        self.game_board = FillerBoard(number_of_colors, height, width, figure=not r_l)
        self.automated = automated
        self.r_l = r_l
        self.save_images_suffix = save_images_suffix

        self.turn_count = 0

        player_1_starting_cell = (height - 1, 0)
        if self.automated:
            self.player_1 = player.AIPlayer([player_1_starting_cell], self.game_board)
        elif self.r_l:
            self.player_1 = player.RLPlayer([player_1_starting_cell], self.game_board)
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
        mask = (self.all_colors != self.player_1.color) & (self.all_colors != self.player_2.color)
        return self.all_colors[mask]

    def check_for_end_of_game(self):
        """
        Checks if the game is over.
        The game is over if the players' scores are greater than the number of cells.

        Returns
        -------
        bool
            True if the game is over, False otherwise
        """
        return self.player_1.score + self.player_2.score >= self.number_of_cells

    def check_for_early_finish(self):
        """
        Checks if the game can be finished early: if one of the players has a score greater \
            than half the number of cells.

        Returns
        -------
        bool
            True if the game is over, False otherwise
        """
        return (self.player_1.score > self.number_of_cells / 2) or (self.player_2.score > self.number_of_cells / 2)

    def play_single_turn(self, action=None):
        """
        Completes a single turn by showing the gameboard, playing each of the players' turns, and printing the result.
        The former and latter are only done if self.r_l is False.

        Parameters
        ----------
        action : int, optional
            the integer for the color to play, when doing RL
        """
        self.turn_count += 1
        if self.save_images_suffix:
            self.game_board.graphical_output(save=True, display=False,
                                             image_suffix=f'{self.save_images_suffix}_{self.turn_count}')
        if not (self.r_l or self.automated):
            self.game_board.graphical_output()

        self.player_1.play_turn([action] if action else self.get_color_options())
        self.player_2.play_turn(self.get_color_options())

        if self.automated:
            self.game_board.graphical_output(save=True, image_suffix=self.turn_count)

        if not self.r_l:
            print(f"player 1 played {self.player_1.color}:  {self.player_1.score}")
            print(f"player 2 played {self.player_2.color}:  {self.player_2.score}")
            print()

    def play_game(self, early_finish=False):
        """
        Completes the entire game by playing turns until the game is over and then prints the result.

        Parameters
        ----------
        early_finish : bool, optional
            determines whether the game can be finished early, by default False
        """
        while not (self.check_for_end_of_game() or (early_finish and self.check_for_early_finish())):
            self.play_single_turn()
            if self.automated:
                input('Press any key to continue.\n')

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

    def __init__(self, number_of_colors, height, width, figure=True):
        self.height = height
        self.width = width
        self.number_of_colors = number_of_colors

        if figure:
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

    def graphical_output(self, block=False, save=False, display=True, folder_name='output', image_suffix=None):
        """
        Outputs the gameboard in a MatPlotLib window that is updated everytime this function is called.
        The 2D numpy array is converted to colors using the COLORS dictionary and then repeated to create an image.

        Parameters
        ----------
        block : bool, optional
            determines whether the MatPlotLib figure blocks code execution, by default False
        save : bool, optional
            determines whether the MatPlotLib figure is saved, by default False
        display : bool, optional
            determines whether the MatPlotLib figure is displayed, by default True
        folder_name : str, optional
            the name of the folder where the image is saved, by default 'output'
        image_suffix : str, optional
            filename suffix for the image, by default None

        Returns
        -------
        np.ndarray
            the image in numpy format with shape (height, width, 3)
        """
        masks = [np.where(self.board == i, True, False) for i in range(self.number_of_colors)]
        output = np.zeros((self.height, self.width, 3), dtype=np.int)
        for mask, color in zip(masks, list(COLORS.values())[:self.number_of_colors]):
            output[mask] = color

        image = np.repeat(np.repeat(output, 10, axis=0), 10, axis=1)/255.0
        if save:
            plt.imsave(f'{folder_name}/image{image_suffix}.png', image)

        if display:
            plt.imshow(image)
            plt.show(block=block)

        return image

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

    def check_if_filled(self, new_cell, cell_color, filled_edges, filled_surrounded):
        """
        Checks if the new cell has the same color.
        If so, then it will be added to filled_edges.

        Parameters
        ----------
        new_cell : tuple
            the coordinates in (y, x) form
        cell_color : int
            the color to check at the new cell
        filled_edges : list
            a list of edge cells that belong to the player
        filled_surrounded : list
            a list of surrounded cells that belong to the player

        Returns
        -------
        bool
            False if the colors don't match, True otherwise
        """
        new_cell_color = self.get_color(new_cell)
        if new_cell_color != cell_color:
            return False

        if new_cell not in filled_edges + filled_surrounded:
            filled_edges.append(new_cell)

        return True

    def update_filled(self, filled_edges, filled_surrounded):
        """
        Updates the list of cells that belong to the player.
        The edge cells will be checked to see if adjoining cells have the same color.
        If a cell is surrounded by the same color, then it will be moved to the
        surrounded cells list and not be checked further.

        Parameters
        ----------
        filled_edges : list
            a list of edge cells that belong to the player
        filled_surrounded : list
            a list of surrounded cells that belong to the player
        """
        surrounded_cells = []
        for cell in filled_edges:
            coord_x = cell[1]
            coord_y = cell[0]
            color = self.get_color(cell)
            surrounded = True

            # up
            if coord_y - 1 >= 0:
                surrounded &= self.check_if_filled((coord_y-1, coord_x), color, filled_edges, filled_surrounded)

            # down
            if coord_y + 1 < self.height:
                surrounded &= self.check_if_filled((coord_y+1, coord_x), color, filled_edges, filled_surrounded)

            # left
            if coord_x - 1 >= 0:
                surrounded &= self.check_if_filled((coord_y, coord_x-1), color, filled_edges, filled_surrounded)

            # right
            if coord_x + 1 < self.width:
                surrounded &= self.check_if_filled((coord_y, coord_x+1), color, filled_edges, filled_surrounded)

            if surrounded:
                surrounded_cells.append(cell)

        for cell in surrounded_cells:
            filled_surrounded.append(cell)
            filled_edges.remove(cell)

    def get_color_count(self, color, filled):
        """
        Counts the number of adjacent cells of the specified color.

        Parameters
        ----------
        color : int
            the color to count in the adjacent cells
        filled : list
            a list of cells that belong to the player

        Returns
        -------
        int
            the number of the adjacent cells with the specified color
        """
        count = 0
        for cell in filled:
            coord_x = cell[1]
            coord_y = cell[0]

            # up
            if coord_y - 1 >= 0:
                new_cell = (coord_y-1, coord_x)
                cell_up_color = self.get_color(new_cell)
                if cell_up_color == color and new_cell not in filled:
                    count += 1
                    filled.append(new_cell)

            # down
            if coord_y + 1 < self.height:
                new_cell = (coord_y+1, coord_x)
                cell_down_color = self.get_color(new_cell)
                if cell_down_color == color and new_cell not in filled:
                    count += 1
                    filled.append(new_cell)

            # left
            if coord_x - 1 >= 0:
                new_cell = (coord_y, coord_x-1)
                cell_left_color = self.get_color(new_cell)
                if cell_left_color == color and new_cell not in filled:
                    count += 1
                    filled.append(new_cell)

            # right
            if coord_x + 1 < self.width:
                new_cell = (coord_y, coord_x+1)
                cell_right_color = self.get_color(new_cell)
                if cell_right_color == color and new_cell not in filled:
                    count += 1
                    filled.append(new_cell)

        return count

    def get_board(self):
        """
        Flattens the gameboard and returns it as a 1D array.

        Returns
        -------
        np.ndarray
            a flat 1D representation of the gameboard
        """
        return self.board.reshape(-1, self.height * self.width)
