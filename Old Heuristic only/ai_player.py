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

        all_points = [(x, y, z) for x in range(4) for y in range(4) for z in range(4)]

        possible_combinations = []
        for p1 in all_points:
            for p2 in all_points:
                for p3 in all_points:
                    for p4 in all_points:
                        if len({p1, p2, p3, p4}) == 4: 
                            possible_combinations.append((p1, p2, p3, p4))
                            if len(possible_combinations) > 1000: 
                                break
                    if len(possible_combinations) > 1000:
                        break
                if len(possible_combinations) > 1000:
                    break
            if len(possible_combinations) > 1000:
                break

        for combination in possible_combinations:
            player_count = 0
            opponent_count = 0

            for x, y, z in combination:
                if game.board[x][y][z] == player:
                    player_count += 1
                elif game.board[x][y][z] is not None:
                    opponent_count += 1
            
            if player_count > 0 and opponent_count == 0:
                score += player_count ** 2
            elif opponent_count > 0 and player_count == 0:
                score -= opponent_count ** 2

        return score
