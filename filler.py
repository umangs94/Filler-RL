import numpy as np

import player


class Filler:
    def __init__(self, number_of_colors, height, width):
        self.number_of_colors = number_of_colors
        self.color_options = np.arange(number_of_colors)
        self.height = height
        self.width = width

        self.board = np.random.randint(0, self.number_of_colors, (self.height, self.width))
        print(self.board)
        print()

        self.player_1 = player.AIPlayer([[self.height - 1, 0]], self.board,
                                        self.height, self.width, self.number_of_colors)
        self.player_2 = player.AIPlayer([[0, self.width - 1]], self.board,
                                        self.height, self.width, self.number_of_colors)

    def get_color_options(self):
        return self.color_options[(self.color_options != self.player_1.current_value) & (self.color_options != self.player_2.current_value)]

    def play_full_game(self):
        while self.player_1.score + self.player_2.score < self.height * self.width:
            self.board = self.player_1.play_turn(self.get_color_options(), self.board)
            self.board = self.player_2.play_turn(self.get_color_options(), self.board)

            print(f"player 1 played {self.player_1.current_value}:  {self.player_1.score}")
            print(f"player 2 played {self.player_2.current_value}:  {self.player_2.score}")
            print(self.board)
            print()

        if self.player_1.score > self.player_2.score:
            print("player 1 wins")
        else:
            print("player 2 wins")


if __name__ == "__main__":
    FILLER = Filler(number_of_colors=8, height=12, width=8)
    FILLER.play_full_game()
