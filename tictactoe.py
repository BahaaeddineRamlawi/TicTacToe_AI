import http.server
import socketserver
import json
from urllib.parse import parse_qs


PORT = 8080
board = [[' ' for _ in range(3)] for _ in range(3)]

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    if any(' ' in row for row in board):
        return None
    return 'Tie'

def minimax(board, depth, is_max):
    if check_winner(board) == 'X':
        return -1
    if check_winner(board) == 'O':
        return 1
    if check_winner(board) == 'Tie':
        return 0

    if is_max:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    max_eval = float('-inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = minimax(board, 0, False)
                board[i][j] = ' '
                if eval > max_eval:
                    max_eval = eval
                    move = (i, j)
    return move

def make_move(i, j):
    if board[i][j] == ' ':
        board[i][j] = 'X'
        move = (3,3)
        if check_winner(board) is None:
            move = best_move(board)
            if move is not None:
                i, j = move
                board[i][j] = 'O'
            if check_winner(board) == 'O':
                return move,"Game Over, You lose!"
            elif check_winner(board) == 'Tie':
                return move,"Game Over, It's a tie!"
            return move,""
        else:
            if check_winner(board) == 'X':
                return move,"Game Over, You win!"
            elif check_winner(board) == 'Tie':
                return move,"Game Over, It's a tie!"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        super().do_GET()

    def do_POST(self):
        global board
        if self.path == '/send_data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            input_data = data.get('data', '')
            print("input_data  ",input_data)  # row and column chosen by the player.
            returndata = make_move(input_data.get('row'), input_data.get('column'))
            (move, text) = returndata
            (row, column) = move
            response_data = {
                "row": row,
                "column": column,
                "text": text
            }
            # if text != '':  #if text not an empty string -> it's a tie or someone have won so we need to reset the game.
            #     board = [[' ' for _ in range(3)] for _ in range(3)]
            print("response_data  ", response_data) # row and column chosen by the AI.
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        elif self.path == '/reset_game':
            self.reset_game()
        else:
            self.send_error(404)
    
    def reset_game(self):
        global board
        board = [[' ' for _ in range(3)] for _ in range(3)]
        response_data = {
            "message": "Game reset successfully"
        }
        print("response_data", response_data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())


with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()