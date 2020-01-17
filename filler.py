import numpy as np

import player


class FillerGame:
    def __init__(self, number_of_colors, height, width):
        self.number_of_colors = number_of_colors
        self.number_of_squares = height * width
        self.color_options = np.arange(number_of_colors)
        self.game_board = FillerBoard(number_of_colors, height, width)
        self.game_board.output()

        player_1_starting_cell = (height - 1, 0)
        self.player_1 = player.AIPlayer([player_1_starting_cell], self.game_board)

        player_2_starting_cell = (0, width - 1)
        self.player_2 = player.AIPlayer([player_2_starting_cell], self.game_board)

    def get_color_options(self):
        mask = (self.color_options != self.player_1.color) & (self.color_options != self.player_2.color)
        options = self.color_options[mask]
        np.random.shuffle(options)

        return options

    def play_automated_game(self):
        while self.player_1.score + self.player_2.score < self.number_of_squares:
            self.player_1.play_turn(self.get_color_options())
            self.player_2.play_turn(self.get_color_options())

            print(f"player 1 played {self.player_1.color}:  {self.player_1.score}")
            print(f"player 2 played {self.player_2.color}:  {self.player_2.score}")
            self.game_board.output()

        if self.player_1.score > self.player_2.score:
            print("player 1 wins")
        elif self.player_2.score > self.player_1.score:
            print("player 2 wins")
        else:
            print('tie')

        return len(np.unique(self.game_board.board)) == 2


class FillerBoard:
    def __init__(self, number_of_colors, height, width):
        self.height = height
        self.width = width

        self.board = np.random.randint(0, number_of_colors, (height, width))

    def output(self):
        print(self.board)
        print()

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
    FILLER = FillerGame(number_of_colors=8, height=12, width=8)

    if input('Enter "y" for AI vs. AI: ') == 'y':
        FILLER.play_automated_game()
