import math

class AIPlayer:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        self.opponent_symbol = "O" if player_symbol == "X" else "X"

    def find_best_move(self, game):
        best_val = -math.inf
        best_move = None

        for move in self.get_available_moves(game):
            x, y, z = move
            game.board[x][y][z] = self.player_symbol
            move_val = self.minimax(game, 1, False) 
            game.board[x][y][z] = None
            if move_val > best_val:
                best_val = move_val
                best_move = move
        return best_move

    def minimax(self, game, depth, maximizing_player):
        if game.is_winner(self.player_symbol):
            return 1000
        if game.is_winner(self.opponent_symbol):
            return -1000
        if game.is_full() or depth == 0:
            return 0

        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_available_moves(game):
                x, y, z = move
                game.board[x][y][z] = self.player_symbol
                eval = self.minimax(game, depth - 1, False)
                game.board[x][y][z] = None
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_available_moves(game):
                x, y, z = move
                game.board[x][y][z] = self.opponent_symbol
                eval = self.minimax(game, depth - 1, True)
                game.board[x][y][z] = None
                min_eval = min(min_eval, eval)
            return min_eval

    def get_available_moves(self, game):
        moves = []
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if game.board[x][y][z] is None:
                        moves.append((x, y, z))
        return moves
