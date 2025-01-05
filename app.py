from flask import Flask, jsonify, request, render_template
import os
import random

app = Flask(__name__)

# Global game state variables
board = [[' ' for _ in range(3)] for _ in range(3)]
counter = 1
max_depth = 9
randomiser = False
alphabeta = True

############  Evaluation Function  ############
def evaluate(board):
    score = 0
    var = check_winner(board)[0]
    if var == 'O':
        score = 10
    elif var == 'X':
        score = -10
    elif var == 'Tie':
        score = 0
    for i in range(3):
        row = [board[i][0], board[i][1], board[i][2]]
        col = [board[0][i], board[1][i], board[2][i]]
        score += score_line(row)
        score += score_line(col)

    diagonal1 = [board[0][0], board[1][1], board[2][2]]
    diagonal2 = [board[0][2], board[1][1], board[2][0]]
    score += score_line(diagonal1)
    score += score_line(diagonal2)
    return score

def score_line(line):
    if line.count('O') == 2 and line.count(' ') == 1:
        return -3
    elif line.count('X') == 2 and line.count(' ') == 1:
        return 3
    else:
        return 0

############  Check Winners  ############
def check_winner(board):
    ending = [(0,0),(0,0),(0,0)]
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != ' ':
            ending = [(row,0),(row,1),(row,2)]
            return (board[row][0],ending)
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            ending = [(0,col),(1,col),(2,col)]
            return (board[0][col],ending)
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        ending = [(0,0),(1,1),(2,2)]
        return (board[0][0],ending)
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        ending = [(0,2),(1,1),(2,0)]
        return (board[0][2],ending)
    if any(' ' in row for row in board):
        return (None, None)
    return ('Tie',ending)

def value(state):
    result, _ = check_winner(state)
    if result == 'X':
        return -100
    elif result == 'O':
        return 100
    elif result == 'Tie':
        return 0
    return None

############  Minimax Functions  ############
def minimax(board, depth, is_max, alpha, beta):
    result = value(board)
    if result is not None or depth >= max_depth:
        if depth >= max_depth:
            return evaluate(board)
        return result
    if is_max:
        return max_value(board, depth, alpha, beta)
    else:
        return min_value(board, depth, alpha, beta)

def max_value(board, depth, alpha, beta):
    max_eval = -float('inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                if depth >= max_depth:
                    return evaluate(board)
                else:
                    eval = minimax(board, depth + 1, False, alpha, beta)
                board[i][j] = ' '
                max_eval = max(max_eval, eval)
                if alphabeta:
                    if eval >= beta:
                        return eval
                    alpha = max(alpha, eval)
    return max_eval

def min_value(board, depth, alpha, beta):
    min_eval = float('inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                if depth >= max_depth:
                    return evaluate(board)
                else:
                    eval = minimax(board, depth + 1, True, alpha, beta)
                board[i][j] = ' '
                min_eval = min(min_eval, eval)
                if alphabeta:
                    if eval <= alpha:
                        return eval
                    beta = min(beta, eval)
    return min_eval

############  AI Move  ############
def best_move(board, depth = 0, alpha = -100, beta = 100):
    if not randomiser:
        max_eval = -float('inf')
        optimal_moves = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth, False, alpha, beta)
                    board[i][j] = ' '
                    if eval > max_eval:
                        max_eval = eval
                        optimal_moves = (i, j)
                    if alphabeta:
                        if eval >= beta:
                            return optimal_moves
                        alpha = max(alpha, eval)
        return optimal_moves
    else:
        available_moves = [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]
        if available_moves:
            row, col = random.choice(available_moves)
            board[row][col] = 'O'
            return row, col
    
def make_move(i, j):
    if board[i][j] == ' ':
        board[i][j] = 'X'
        move = (3,3)
        result, box = check_winner(board)
        if result is None:
            move = best_move(board)
            if move is not None:
                i, j = move
                board[i][j] = 'O'
            result, box = check_winner(board)
            if result == 'O':
                return move, "AI won the game!", box
            elif result == 'Tie':
                return move, "Game Over, It's a tie!", box
            return move, "", box
        else:
            if result == 'X':
                return move, "You won the game!", box
            elif result == 'Tie':
                return move, "Game Over, It's a tie!", box

############  Flask Routes  ############

@app.route('/send_data', methods=['POST'])
def send_data():
    global counter
    data = request.get_json()
    row, column = data['data']['row'], data['data']['column']
    print(f"------------------------------------\n| {counter} - You ->  row: {row}, column: {column} |")
    counter += 1
    move, text, box = make_move(row, column)
    response_data = {
        "row": move[0],
        "column": move[1],
        "text": text,
        "box": box
    }
    if text in ('', 'AI won the game!'):
        print(f"| {counter} - AI  ->  row: {move[0]}, column: {move[1]} |")
        print("------------------------------------")
        counter += 1
    else:
        print("------------------------------------")
    if text: print(f"\n>>  Result -> {text}\n")
    return jsonify(response_data)

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global board, counter
    board = [[' ' for _ in range(3)] for _ in range(3)]
    counter = 1
    return jsonify({"message": "Game reset successfully"})

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    global max_depth, randomiser
    data = request.get_json()
    difficulty = data['data']['difficulty']
    print(f"\n>>  Set Difficulty: -> {difficulty}")
    if difficulty == 'Impossible':
        max_depth = 9
        randomiser = False
    elif difficulty == 'Medium':
        max_depth = 1
        randomiser = False
    else:
        randomiser = True
    return jsonify({"status": "Difficulty set successfully!"})

@app.route('/set_pruning', methods=['POST'])
def set_pruning():
    global alphabeta
    data = request.get_json()
    alphabeta = data['data']['alphabeta']
    print(f">>  Set Pruning: -> {alphabeta}")
    return jsonify({"status": "Pruning set successfully!"})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
