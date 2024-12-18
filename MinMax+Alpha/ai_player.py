import math

class AIPlayer:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        self.opponent_symbol = "O" if player_symbol == "X" else "X"

    def find_best_move(self, game):
        best_val = -math.inf
        best_move = None

        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if game.board[x][y][z] is None:
                        game.board[x][y][z] = self.player_symbol
                        move_val = self.minimax(game, 2, -math.inf, math.inf, False)  
                        game.board[x][y][z] = None
                        if move_val > best_val:
                            best_val = move_val
                            best_move = (x, y, z)
        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if game.is_winner(self.player_symbol):
            return 1000 - (3 - depth)  
        if game.is_winner(self.opponent_symbol):
            return -1000 + (3 - depth)  
        if game.is_full() or depth == 0:
            return 0  

        if maximizing_player:
            max_eval = -math.inf
            for x in range(4):
                for y in range(4):
                    for z in range(4):
                        if game.board[x][y][z] is None:
                            game.board[x][y][z] = self.player_symbol
                            eval = self.minimax(game, depth - 1, alpha, beta, False)
                            game.board[x][y][z] = None
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                return max_eval
            return max_eval
        else:
            min_eval = math.inf
            for x in range(4):
                for y in range(4):
                    for z in range(4):
                        if game.board[x][y][z] is None:
                            game.board[x][y][z] = self.opponent_symbol
                            eval = self.minimax(game, depth - 1, alpha, beta, True)
                            game.board[x][y][z] = None
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                return min_eval
            return min_eval
