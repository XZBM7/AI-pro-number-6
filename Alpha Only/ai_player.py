import math

class AIPlayer:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        self.opponent_symbol = "O" if player_symbol == "X" else "X"

    def find_best_move(self, game):
        def alpha_beta_pruning(depth, alpha, beta, current_player):
            if game.is_winner(self.player_symbol):
                return 1000
            if game.is_winner(self.opponent_symbol):
                return -1000
            if game.is_full() or depth == 0:
                return 0

            if current_player == self.player_symbol:
                best_value = -math.inf
                for x in range(4):
                    for y in range(4):
                        for z in range(4):
                            if game.board[x][y][z] is None:
                                game.board[x][y][z] = self.player_symbol
                                value = alpha_beta_pruning(depth - 1, alpha, beta, self.opponent_symbol)
                                game.board[x][y][z] = None
                                best_value = max(best_value, value)
                                alpha = max(alpha, value)
                                if beta <= alpha:
                                    return best_value
                return best_value
            else:
                best_value = math.inf
                for x in range(4):
                    for y in range(4):
                        for z in range(4):
                            if game.board[x][y][z] is None:
                                game.board[x][y][z] = self.opponent_symbol
                                value = alpha_beta_pruning(depth - 1, alpha, beta, self.player_symbol)
                                game.board[x][y][z] = None
                                best_value = min(best_value, value)
                                beta = min(beta, value)
                                if beta <= alpha:
                                    return best_value
                return best_value

        best_val = -math.inf
        best_move = None

        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if game.board[x][y][z] is None:
                        game.board[x][y][z] = self.player_symbol
                        move_val = alpha_beta_pruning(2, -math.inf, math.inf, self.opponent_symbol)  # عمق البحث 2
                        game.board[x][y][z] = None
                        if move_val > best_val:
                            best_val = move_val
                            best_move = (x, y, z)

        return best_move
