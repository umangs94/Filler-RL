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

        self.player_1 = player.AIPlayer([[self.height - 1, 0]], self.board,
                                        self.height, self.width, self.number_of_colors)
        self.player_2 = player.AIPlayer([[0, self.width - 1]], self.board,
                                        self.height, self.width, self.number_of_colors)

    def get_color_options(self):
        return self.color_options[(self.color_options != self.player_1.current_value) & (self.color_options != self.player_2.current_value)]

    def best_turn(self):
        player_1_value = self.player_1.get_action(self.get_color_options(), self.board)
        self.board = self.player_1.set_filled(player_1_value, self.board)

        print(f"player 1 played {player_1_value}:  {self.player_1.score}")
        print(self.board)

        player_2_value = self.player_2.get_action(self.get_color_options(), self.board)
        self.board = self.player_2.set_filled(player_2_value, self.board)

        print(f"player 2 played {player_2_value}:  {self.player_2.score}")
        print(self.board)
        print()

    def play_full_game(self):
        while self.player_1.score + self.player_2.score < self.height * self.width:
            self.best_turn()

        if self.player_1.score > self.player_2.score:
            print("player 1 wins")
        else:
            print("player 2 wins")


if __name__ == "__main__":
    FILLER = Filler(number_of_colors=8, height=12, width=8)
    FILLER.play_full_game()
