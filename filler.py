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
    def __init__(self, number_of_colors, height, width, automated):
        self.number_of_colors = number_of_colors
        self.number_of_squares = height * width
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
        mask = (self.color_options != self.player_1.color) & (self.color_options != self.player_2.color)
        return self.color_options[mask]

    def play(self):
        while self.player_1.score + self.player_2.score < self.number_of_squares:
            self.player_1.play_turn(self.get_color_options())
            self.player_2.play_turn(self.get_color_options())

            print(f"player 1 played {self.player_1.color}:  {self.player_1.score}")
            print(f"player 2 played {self.player_2.color}:  {self.player_2.score}")
            print()

            if self.automated:
                self.game_board.graphical_output(block=True)

        if self.player_1.score > self.player_2.score:
            print("player 1 wins!" if AUTOMATED else "you win!")
        elif self.player_2.score > self.player_1.score:
            print("player 2 wins!" if AUTOMATED else "you lose!")
        else:
            print("it was a tie!")
        self.game_board.graphical_output()

        return len(np.unique(self.game_board.board)) == 2


class FillerBoard:
    def __init__(self, number_of_colors, height, width):
        self.height = height
        self.width = width
        self.number_of_colors = number_of_colors

        self.board = np.random.randint(0, number_of_colors, (height, width))

    def output(self):
        print(self.board)
        print()

    def graphical_output(self, block=False):
        masks = [np.where(self.board == i, True, False) for i in range(self.number_of_colors)]
        output = np.zeros((self.height, self.width, 3), dtype=np.int)
        for mask, color in zip(masks, list(COLORS.values())[:self.number_of_colors]):
            output[mask] = color

        output = np.repeat(np.repeat(output, 10, axis=0), 10, axis=1)
        plt.imsave('image.png', output)

        plt.close('all')
        plt.imshow(output)
        plt.show(block=block)

    def get_color(self, coord):
        return self.board[coord[0], coord[1]]

    def set_color(self, color, filled):
        for cell in filled:
            self.board[cell[0], cell[1]] = color

    def update_filled(self, filled):
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


if __name__ == "__main__":
    AUTOMATED = input('Enter "y" for AI vs. AI: ') == 'y'
    FILLER = FillerGame(number_of_colors=8, height=12, width=8, automated=AUTOMATED)
    FILLER.play()
