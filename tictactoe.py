import http.server
import socketserver
import json
from urllib.parse import parse_qs


PORT = 8080
board = [[' ' for _ in range(3)] for _ in range(3)]
counter = 1;

def check_winner(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != ' ':
            return (board[row][0],[(row,0),(row,1),(row,2)])
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return (board[0][col],[(0,col),(1,col),(2,col)])
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return (board[0][0],[(0,0),(1,1),(2,2)])
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return (board[0][2],[(0,2),(1,1),(2,0)])
    if any(' ' in row for row in board):
        return (None, None)
    return ('Tie',[(0,0),(0,0),(0,0)])

def value(state):
    result,_ = check_winner(state)
    if result == 'X':
        return -1
    elif result == 'O':
        return 1
    elif result == 'Tie':
        return 0
    return None

def minimax(board, depth, is_max, alpha, beta):
    result = value(board)
    if result is not None:
        return result

    if is_max:
        return max_value(board, depth, alpha, beta)
    else:
        return min_value(board, depth, alpha, beta)

def max_value(board, depth, alpha, beta):
    max_eval = -2
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i][j] = ' '
                max_eval = max(max_eval, eval)
                if eval >= beta:
                    return eval
                alpha = max(alpha, eval)
    return max_eval

def min_value(board, depth, alpha, beta):
    min_eval = 2
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[i][j] = ' '
                min_eval = min(min_eval, eval)
                if eval <= alpha:
                    return eval
                beta = min(beta, eval)
    return min_eval



def best_move(board):
    max_eval = -2
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = minimax(board, 0, False, -2, 2)
                board[i][j] = ' '
                if eval > max_eval:
                    max_eval = eval
                    move = (i, j)
    return move

def make_move(i, j):
    if board[i][j] == ' ':
        board[i][j] = 'X'
        move = (3,3)
        result,box = check_winner(board)
        if result is None:
            move = best_move(board)
            if move is not None:
                i, j = move
                board[i][j] = 'O'
            result,box = check_winner(board)
            if result == 'O':
                return move,"AI won the game!",box
            elif result == 'Tie':
                return move,"Game Over, It's a tie!",box
            return move,"",box
        else:
            if result == 'X':
                return move,"You won the game!",box
            elif result == 'Tie':
                return move,"Game Over, It's a tie!",box

class CustomHandler(http.server.SimpleHTTPRequestHandler): #POST and GET APIs
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        super().do_GET()

    def do_POST(self):
        global board,counter
        if self.path == '/send_data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            input_data = data.get('data', '')
            print("-----------------------------------------")
            print("|",counter,"- You ->  ",input_data," |")  # row and column chosen by the player.
            counter += 1
            returndata = make_move(input_data.get('row'), input_data.get('column'))
            (move, text, box) = returndata
            (row, column) = move
            response_data = {
                "row": row,
                "column": column,
                "text": text,
                "box": box
            }
            if counter < 9:
                print("|",counter,"- AI  ->  ", {"row":row,"column":column}," |") # row and column chosen by the AI.
                print("-----------------------------------------")
                counter += 1
            else:
                print("-----------------------------------------")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        elif self.path == '/reset_game':
            self.reset_game()
        else:
            self.send_error(404)
    
    def reset_game(self):
        global board,counter
        board = [[' ' for _ in range(3)] for _ in range(3)]
        counter = 1
        response_data = {
            "message": "Game reset successfully"
        }
        print("Reset:  ->  ", response_data["message"])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())


with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()