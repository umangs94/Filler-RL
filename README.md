# Filler

I created this project to experiment with creating an RL agent to beat the game Filler (example: <https://apkpure.com/filler-game/org.caeex.filler).>

Currently, the player can play against an AI player or let it play against another AI player.
The AI player does a depth-first search (DFS) to select the best action to take.

## How to play

Run `python filler.py` to play.

Press `y` to watch as the AI player competes against another AI player. Press `q` in the MatPlotLib window to see the next turn.

Press `return` or any other key to play manually against the AI player. The MatPlotLib window will show the current game state. Enter your color choice in the Terminal window.

## More details

To create an RL agent that can beat this game, first I had to code up the actual game in Python. I created multiple classes to store the game, the players, and the values on the board. The gameboard values are kept as integers on the backend and displayed in color using MatPlotLib.

An image of the gameboard is saved as `image.png` each turn. This will be used as the state when I begin training the RL agent. The action will be the color to play next and the reward will be the player's score.

I anticipate a challenge for the agent as playing manually, there are times when the current DFS agent can beat me easily. Nevertheless, I can always increase the DFS' depth to improve the AI and create a tougher challenge.
