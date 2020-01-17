import numpy as np


class Player:
    def __init__(self, filled, game_board, game_height, game_width, game_number_of_colors):
        self.filled = filled
        self.score = 1
        self.current_value = game_board[filled[0][0], filled[0][1]]
        self.game_height = game_height
        self.game_width = game_width
        self.game_number_of_colors = game_number_of_colors
        self.filled = self.update_filled(game_board, self.filled)

    def update_filled(self, game_board, filled):
        for cell in filled:
            coord_x = cell[1]
            coord_y = cell[0]
            cell_value = game_board[coord_y, coord_x]

            # up
            if coord_y - 1 >= 0:
                new_cell = [coord_y-1, coord_x]
                cell_above_value = game_board[coord_y-1, coord_x]
                if cell_value == cell_above_value and new_cell not in filled:
                    filled.append(new_cell)

            # down
            if coord_y + 1 < self.game_height:
                new_cell = [coord_y+1, coord_x]
                cell_down_value = game_board[coord_y+1, coord_x]
                if cell_value == cell_down_value and new_cell not in filled:
                    filled.append(new_cell)

            # left
            if coord_x - 1 >= 0:
                new_cell = [coord_y, coord_x-1]
                cell_left_value = game_board[coord_y, coord_x-1]
                if cell_value == cell_left_value and new_cell not in filled:
                    filled.append(new_cell)

            # right
            if coord_x + 1 < self.game_width:
                new_cell = [coord_y, coord_x+1]
                cell_right_value = game_board[coord_y, coord_x+1]
                if cell_value == cell_right_value and new_cell not in filled:
                    filled.append(new_cell)

        return filled

    def set_filled(self, value, game_board):
        assert value < self.game_number_of_colors, "Invalid value"

        for cell in self.filled:
            game_board[cell[0], cell[1]] = value
        self.filled = self.update_filled(game_board, self.filled.copy())
        self.score = len(self.filled)
        self.current_value = value

        return game_board

    def simulate_filled(self, value, game_board):
        assert value < self.game_number_of_colors, "Invalid value"

        for cell in self.filled:
            game_board[cell[0], cell[1]] = value
        filled = self.update_filled(game_board, self.filled.copy())
        score = len(filled)

        return score

    def get_action(self, color_options, game_board):
        raise NotImplementedError


class AIPlayer(Player):
    def get_action(self, color_options, game_board):
        max_score = -1
        best_option = -1
        for option in color_options:
            simulated_score = self.simulate_filled(option, game_board.copy())
            if simulated_score > max_score:
                max_score = simulated_score
                best_option = option

        return best_option


class RandomPlayer(Player):
    def get_action(self, color_options, game_board):
        return np.random.choice(color_options)
