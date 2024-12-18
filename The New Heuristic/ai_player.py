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
                        move_val = self.minimax(game, 1, -math.inf, math.inf, False)
                        game.board[x][y][z] = None
                        if move_val > best_val:
                            best_val = move_val
                            best_move = (x, y, z)
        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if game.is_winner(self.player_symbol):
            return 1000
        if game.is_winner(self.opponent_symbol):
            return -1000
        if game.is_full() or depth == 0:
            return self.heuristic(game, self.player_symbol) - self.heuristic(game, self.opponent_symbol)

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
                                break
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
                                break
            return min_eval

    def heuristic(self, game, player):
        score = 0
        directions = [   ## الاحداثيات x , y , z     
            (1, 0, 0), (0, 1, 0), (0, 0, 1),    ##(1, 0, 0) z, (0, 1, 0) y, (0, 0, 1) x,
            (1, 1, 0), (1, 0, 1), (0, 1, 1),    ## (1, 1, 0) y z, (1, 0, 1) x z, (0, 1, 1) x y,
            (1, 1, 1), (1, -1, 0), (1, 0, -1),
            (0, 1, -1), (1, -1, -1)
        ]

        for x in range(4):
            for y in range(4):
                for z in range(4):
                    for dx, dy, dz in directions:
                        count = 0
                        for i in range(4):
                            nx, ny, nz = x + i * dx, y + i * dy, z + i * dz
                            if 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4:
                                if game.board[nx][ny][nz] == player:
                                    count += 1
                                elif game.board[nx][ny][nz] is not None:
                                    count = 0
                                    break
                        if count > 0:
                            score += count ** 2
        return score
