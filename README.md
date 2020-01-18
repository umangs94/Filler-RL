# Filler

I created this project to experiment with creating an RL agent to beat the game Filler (example: <https://apkpure.com/filler-game/org.caeex.filler).>

Currently, the player can play against an AI player or let it play against another AI player.
The AI player does a depth-first search to select the best action to take.

## How to play

Run `python filler.py` to play.

Press `y` to watch as the AI player competes against another AI player. Press `q` in the MatPlotLib window to see the next turn.

Press `return` or any other key to play manually against the AI player. The MatPlotLib window will show the current game state. Enter your color choice in the Terminal window.

## More details

To create an RL agent that can beat this game, first I had to code up the actual game in Python. I created multiple classes to store the game, the players, and the values on the board.

The gameboard values are kept as integers on the backend and displayed in color using MatPlotLib.
