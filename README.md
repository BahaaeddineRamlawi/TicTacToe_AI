# TicTacToe_AI

This project is a straightforward implementation of the classic Tic-Tac-Toe game with an AI opponent. It allows users to play against the computer, which employs a minimax algorithm for intelligent moves. Additionally, the AI supports depth-limited search and alpha-beta pruning, enhancing the capabilities of the minimax algorithm.
The game offers an interactive and enjoyable experience for all players.

## Usage

Clone the project repository to your local machine:
```
git clone https://github.com/BahaaeddineRamlawi/TicTacToe_AI.git
```
Navigate to the project directory:
```
cd TicTacToe_AI-main
```

### Running the Game
```
python tictactoe.py
```
Open your web browser and go to http://localhost:8080/index.html to play the game.

Additionally, you can run the server using your preferred browser (Chrome, Edge, or Firefox) only by executing the respective script, to make it easier for you.

### Gameplay

Click on the 'Player X' or 'Player O' button to choose your side.
Select the difficulty level:
- Easy: The opponents make random moves.
- Medium: The opponent follows a depth-limited search with a maximum depth of 1.
- Impossible: Choose between using alpha-beta pruning or following the minimax algorithm.

Tap on the grid cells to make your move. The AI opponent will take its turn automatically.
The game will announce the winner or declare a draw when the game ends.
To reset the game, click the **Replay** button.
For a game review, select the **Review** button at the end of the game.

Enjoy playing Tic-Tac-Toe against the AI and see if you can beat it!

> [!IMPORTANT]
> Hey, just a heads up: the Python server uses a specific socket port, so it's important to stop it properly before running it again. The port can't be reused unless the server is stopped..

#### Credits

> Bahaaeddine Ramlawi <br />
> Ahmad Chaachouh <br />
> Hajar Kattaa
