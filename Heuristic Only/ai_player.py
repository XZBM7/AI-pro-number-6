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
                        move_val = self.heuristic(game, self.player_symbol) - self.heuristic(game, self.opponent_symbol)
                        game.board[x][y][z] = None
                        if move_val > best_val:
                            best_val = move_val
                            best_move = (x, y, z)
        return best_move

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
                        empty_count = 0

                        for i in range(4):
                            nx, ny, nz = x + i * dx, y + i * dy, z + i * dz
                            if 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4:
                                if game.board[nx][ny][nz] == player:
                                    player_count += 1
                                elif game.board[nx][ny][nz] == self.opponent_symbol:
                                    opponent_count += 1
                                else:
                                    empty_count += 1

                        if player_count > 0 and opponent_count == 0:
                            score += player_count ** 3  
                        if opponent_count > 0 and player_count == 0:
                            score -= opponent_count ** 3  
                        if player_count == 3 and empty_count == 1:
                            score += 50  
                        if opponent_count == 3 and empty_count == 1:
                            score -= 100 

        return score
