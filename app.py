from flask import Flask, request, jsonify, send_from_directory
import random
import copy

app = Flask(__name__, static_url_path='', static_folder='.')

# Global game instance (for simplicity, one session at a time)
game = None

class TicTacToeGame:
    def __init__(self, mode, user_player, playerXName="Player X", playerOName="Player O", userName="Player"):
        self.mode = mode  # "multi", "easy", "medium", "hard"
        self.user_player = user_player  # Only used for single-player modes
        self.board = [''] * 9
        self.game_active = True
        self.match_completed = False
        self.current_player = random.choice(['X', 'O'])
        self.scoreX = 0
        self.scoreO = 0
        self.draws = 0
        self.gameCount = 0
        if mode == "multi":
            self.playerXName = playerXName
            self.playerOName = playerOName
        else:
            self.userName = userName
        self.message = f"{self.get_player_name(self.current_player)}'s turn"
        # If in single-player and computer starts, make the computer move.
        if self.mode != "multi" and self.current_player != self.user_player:
            self.ai_move_if_needed()

    def to_dict(self):
        if self.mode == "multi":
            scoreboard = f"Games: {self.gameCount}/10 | {self.playerXName} (X) Wins: {self.scoreX} | {self.playerOName} (O) Wins: {self.scoreO} | Draws: {self.draws}"
        else:
            if self.user_player == 'X':
                userWins, compWins = self.scoreX, self.scoreO
            else:
                userWins, compWins = self.scoreO, self.scoreX
            scoreboard = f"Games: {self.gameCount}/10 | {self.userName} ({self.user_player}) Wins: {userWins} | Computer ({'O' if self.user_player=='X' else 'X'}) Wins: {compWins} | Draws: {self.draws}"
        return {
            "board": self.board,
            "current_player": self.current_player,
            "message": self.message,
            "scoreboard": scoreboard,
            "game_active": self.game_active,
            "match_completed": self.match_completed,
            "mode": self.mode,
            "user_player": self.user_player
        }

    def reset_board(self):
        self.board = [''] * 9
        self.game_active = True
        self.current_player = random.choice(['X', 'O'])
        self.message = f"{self.get_player_name(self.current_player)}'s turn"

    def get_player_name(self, symbol):
        if self.mode == "multi":
            return self.playerXName if symbol == "X" else self.playerOName
        else:
            return self.userName if symbol == self.user_player else "Computer"

    def check_winner(self, board_state=None):
        board_state = board_state if board_state is not None else self.board
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for pattern in win_patterns:
            a, b, c = pattern
            if board_state[a] != '' and board_state[a] == board_state[b] == board_state[c]:
                return board_state[a]
        return None

    def board_full(self):
        return all(cell != '' for cell in self.board)

    def update_score(self, winner):
        if winner == 'X':
            self.scoreX += 1
        elif winner == 'O':
            self.scoreO += 1
        self.gameCount += 1

    def make_move(self, index):
        if self.board[index] == '' and self.game_active and not self.match_completed:
            self.board[index] = self.current_player
            winner = self.check_winner()
            if winner:
                self.message = f"{self.get_player_name(self.current_player)} Wins!"
                self.update_score(winner)
                self.game_active = False
                self.check_match_complete()
            elif self.board_full():
                self.message = "It's a Draw!"
                self.draws += 1
                self.gameCount += 1
                self.game_active = False
                self.check_match_complete()
            else:
                # Switch turn
                self.current_player = 'X' if self.current_player == 'O' else 'O'
                self.message = f"{self.get_player_name(self.current_player)}'s turn"
            return True
        return False

    def computer_move_easy(self):
        empty = [i for i, cell in enumerate(self.board) if cell == '']
        return random.choice(empty) if empty else None

    def computer_move_medium(self):
        comp = 'O' if self.user_player == 'X' else 'X'
        opp = self.user_player
        empty = [i for i, cell in enumerate(self.board) if cell == '']
        # Try winning move
        for i in empty:
            self.board[i] = comp
            if self.check_winner() == comp:
                self.board[i] = ''
                return i
            self.board[i] = ''
        # Block opponent win
        for i in empty:
            self.board[i] = opp
            if self.check_winner() == opp:
                self.board[i] = ''
                return i
            self.board[i] = ''
        return random.choice(empty) if empty else None

    def minimax(self, board_state, player, depth=0):
        ai = 'O' if self.user_player == 'X' else 'X'
        opp = self.user_player
        winner = self.check_winner(board_state)
        if winner == opp:
            return {'score': -10 + depth}
        elif winner == ai:
            return {'score': 10 - depth}
        elif all(cell != '' for cell in board_state):
            return {'score': 0}

        moves = []
        for i, cell in enumerate(board_state):
            if cell == '':
                move = {}
                move['index'] = i
                board_state[i] = player
                if player == ai:
                    result = self.minimax(board_state, opp, depth + 1)
                    move['score'] = result['score']
                else:
                    result = self.minimax(board_state, ai, depth + 1)
                    move['score'] = result['score']
                board_state[i] = ''
                moves.append(move)

        if player == ai:
            bestScore = -9999
            bestMoves = []
            for m in moves:
                if m['score'] > bestScore:
                    bestScore = m['score']
                    bestMoves = [m]
                elif m['score'] == bestScore:
                    bestMoves.append(m)
        else:
            bestScore = 9999
            bestMoves = []
            for m in moves:
                if m['score'] < bestScore:
                    bestScore = m['score']
                    bestMoves = [m]
                elif m['score'] == bestScore:
                    bestMoves.append(m)
        return random.choice(bestMoves)

    def computer_move_hard(self):
        ai = 'O' if self.user_player == 'X' else 'X'
        best_move = self.minimax(copy.deepcopy(self.board), ai)
        return best_move['index'] if best_move and 'index' in best_move else None

    def ai_move_if_needed(self):
        # Only in single-player mode if it’s not the user's turn.
        if self.mode != "multi" and self.game_active and self.current_player != self.user_player:
            if self.mode == 'easy':
                move = self.computer_move_easy()
            elif self.mode == 'medium':
                move = self.computer_move_medium()
            elif self.mode == 'hard':
                move = self.computer_move_hard()
            else:
                move = None
            if move is not None:
                self.make_move(move)

    def new_game(self):
        self.reset_board()
        # If in single player mode and computer should move first, trigger AI.
        if self.mode != "multi" and self.current_player != self.user_player:
            self.ai_move_if_needed()

    def reset_match(self):
        self.scoreX = 0
        self.scoreO = 0
        self.draws = 0
        self.gameCount = 0
        self.match_completed = False
        self.reset_board()
        if self.mode != "multi" and self.current_player != self.user_player:
            self.ai_move_if_needed()

    def check_match_complete(self):
        if self.gameCount >= 10:
            self.match_completed = True
            if self.scoreX > self.scoreO:
                if self.mode == "multi":
                    self.message += f"<br>{self.playerXName} wins the match!"
                else:
                    self.message += f"<br>{self.userName if self.user_player=='X' else 'Computer'} wins the match!"
            elif self.scoreO > self.scoreX:
                if self.mode == "multi":
                    self.message += f"<br>{self.playerOName} wins the match!"
                else:
                    self.message += f"<br>{self.userName if self.user_player=='O' else 'Computer'} wins the match!"
            else:
                self.message += "<br>The match is a draw!"

@app.route('/start', methods=['POST'])
def start():
    global game
    data = request.get_json()
    mode = data.get("mode", "multi")
    user_player = data.get("user_player", "X")
    if mode == "multi":
        playerXName = data.get("playerXName", "Player X")
        playerOName = data.get("playerOName", "Player O")
        game = TicTacToeGame(mode, user_player, playerXName=playerXName, playerOName=playerOName)
    else:
        userName = data.get("userName", "Player")
        game = TicTacToeGame(mode, user_player, userName=userName)
    return jsonify(game.to_dict())

@app.route('/move', methods=['POST'])
def move():
    global game
    data = request.get_json()
    index = data.get("index")
    if game and index is not None:
        game.make_move(index)
        # In single-player mode, if game is still active, trigger AI move.
        if game.mode != "multi" and game.game_active and game.current_player != game.user_player:
            game.ai_move_if_needed()
    return jsonify(game.to_dict())

@app.route('/next', methods=['POST'])
def next_game():
    global game
    if game:
        if game.match_completed:
            game.reset_match()
        else:
            game.new_game()
    return jsonify(game.to_dict())

# Serve the index.html file.
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
