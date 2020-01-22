"""
Use this file to run the game.
"""

from filler import FillerGame

if __name__ == "__main__":
    AUTOMATED = input('Enter "y" for AI vs. AI: ') == 'y'
    FILLER = FillerGame(number_of_colors=8, height=12, width=8,
                        game_type=FillerGame.game_types['vs_ai' if AUTOMATED else 'human'])
    FILLER.play_game()
