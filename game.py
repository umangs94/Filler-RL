"""
Use this file to run the game.
"""

from filler import FillerGame

if __name__ == "__main__":
    AUTOMATED = input('Enter "y" for AI vs. AI: ') == 'y'
    FILLER = FillerGame(number_of_colors=8, height=12, width=8, automated=AUTOMATED)
    FILLER.play_game()
