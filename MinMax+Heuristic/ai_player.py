import math

class AIPlayer:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        self.opponent_symbol = "O" if player_symbol == "X" else "X"

    def find_best_move(self, game):
        best_val = -math.inf
        best_move = None

        moves_to_check = self.get_important_moves(game)

        for x, y, z in moves_to_check:
            if game.board[x][y][z] is None:
                game.board[x][y][z] = self.player_symbol
                move_val = self.minimax(game, 2, True) 
                game.board[x][y][z] = None
                if move_val > best_val:
                    best_val = move_val
                    best_move = (x, y, z)
        return best_move

    def minimax(self, game, depth, maximizing_player):
        if game.is_winner(self.player_symbol):
            return 1000
        if game.is_winner(self.opponent_symbol):
            return -1000
        if game.is_full() or depth == 0:
            return self.heuristic(game, self.player_symbol) - self.heuristic(game, self.opponent_symbol)

        if maximizing_player:
            max_eval = -math.inf
            for x, y, z in self.get_important_moves(game):
                if game.board[x][y][z] is None:
                    game.board[x][y][z] = self.player_symbol
                    eval = self.minimax(game, depth - 1, False)
                    game.board[x][y][z] = None
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for x, y, z in self.get_important_moves(game):
                if game.board[x][y][z] is None:
                    game.board[x][y][z] = self.opponent_symbol
                    eval = self.minimax(game, depth - 1, True)
                    game.board[x][y][z] = None
                    min_eval = min(min_eval, eval)
            return min_eval

    def get_important_moves(self, game):
        important_moves = set()
        directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1),
            (1, 1, 1), (1, -1, 0), (1, 0, -1),
            (0, 1, -1), (1, -1, -1)
        ]

        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if game.board[x][y][z] is not None:
                        for dx, dy, dz in directions:
                            for step in range(-1, 2):  
                                nx, ny, nz = x + step * dx, y + step * dy, z + step * dz
                                if 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4:
                                    important_moves.add((nx, ny, nz))

        return important_moves

    def heuristic(self, game, player):
        score = 0
        directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1),
            (1, 1, 1), (1, -1, 0), (1, 0, -1),
            (0, 1, -1), (1, -1, -1)
        ]

        for x in range(4):
            for y in range(4):
                for z in range(4):
                    for dx, dy, dz in directions:
                        player_count = 0
                        opponent_count = 0

                        for i in range(4):
                            nx, ny, nz = x + i * dx, y + i * dy, z + i * dz
                            if 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4:
                                if game.board[nx][ny][nz] == player:
                                    player_count += 1
                                elif game.board[nx][ny][nz] == self.opponent_symbol:
                                    opponent_count += 1

                        if player_count > 0 and opponent_count == 0:
                            score += player_count ** 2
                        if opponent_count > 0 and player_count == 0:
                            score -= opponent_count ** 2

        return score
