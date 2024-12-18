import math
import numpy as np


class AIPlayer:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        self.opponent_symbol = "O" if player_symbol == "X" else "X"
        self.seen_states = {}

    def rotate_board_90(self, board, axis):
        board = np.array(board)
        if axis == "x":
            return np.rot90(board, axes=(1, 2))
        elif axis == "y":
            return np.rot90(board, axes=(0, 2))
        elif axis == "z":
            return np.rot90(board, axes=(0, 1))
        else:
            raise ValueError(f"Invalid axis: {axis}")

    def reflect_board(self, board, plane):
        board = np.array(board)
        if plane == "xy":
            return np.flip(board, axis=2)
        elif plane == "xz":
            return np.flip(board, axis=1)
        elif plane == "yz":
            return np.flip(board, axis=0)
        else:
            raise ValueError(f"Invalid plane: {plane}")

    # def canonical_form(self, board):
    #     board = np.array(board)
    #     transformations = []
    #
    #     # Generate rotations
    #     for axis in ["x", "y", "z"]:
    #         temp_board = board.copy()  # Avoid modifying the original board
    #         for _ in range(4):
    #             try:
    #                 temp_board = self.rotate_board_90(temp_board, axis)
    #                 transformations.append(tuple(tuple(tuple(row) for row in layer) for layer in temp_board.tolist()))
    #             except ValueError as e:
    #                 print(f"Error rotating board on axis {axis}: {e}")
    #
    #     # Generate reflections
    #     for plane in ["xy", "xz", "yz"]:
    #         try:
    #             reflected = self.reflect_board(board, plane)
    #             transformations.append(tuple(tuple(tuple(row) for row in layer) for layer in reflected.tolist()))
    #         except ValueError as e:
    #             print(f"Error reflecting board on plane {plane}: {e}")
    #
    #     # Ensure valid transformations
    #     transformations = [t for t in transformations if t is not None]
    #
    #     if not transformations:
    #         raise ValueError("No valid transformations generated for canonical form.")
    #
    #     return transformations
    def canonical_form(self, board):
        board = np.array(board)
        transformations = []

        # Generate rotations
        for axis in ["x", "y", "z"]:
            temp_board = board.copy()  # Avoid modifying the original board
            for _ in range(4):
                try:
                    temp_board = self.rotate_board_90(temp_board, axis)
                    transformations.append(tuple(tuple(tuple(row) for row in layer) for layer in temp_board.tolist()))
                except ValueError as e:
                    print(f"Error rotating board on axis {axis}: {e}")

        # Generate reflections
        for plane in ["xy", "xz", "yz"]:
            try:
                reflected = self.reflect_board(board, plane)
                transformations.append(tuple(tuple(tuple(row) for row in layer) for layer in reflected.tolist()))
            except ValueError as e:
                print(f"Error reflecting board on plane {plane}: {e}")

        # Ensure valid transformations
        transformations = [t for t in transformations if t is not None]

        if not transformations:
            raise ValueError("No valid transformations generated for canonical form.")

        # Print all transformations for debugging
        # print("Generated Transformations:")
        # for t in transformations:
        #     print(np.array(t))

        return transformations

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
        # Convert canonical forms to a hashable representation
        # canonical_forms = self.canonical_form(game.board)
        # canonical = tuple(
        #     tuple(tuple(row) for row in layer) for layer in canonical_forms[0])  # Use the first canonical form
        #
        # if canonical in self.seen_states:
        #     return self.seen_states[canonical]

        canonical_forms = self.canonical_form(game.board)
        canonical = tuple(
            tuple(tuple(row) for row in layer) for layer in canonical_forms[0])  # Use the first canonical form

        # Debug canonical state
        # print(f"Canonical state at depth {depth}:")
        # print(np.array(canonical))


        if canonical in self.seen_states:
            print("Using cached value.")
            return self.seen_states[canonical]

        if game.is_winner(self.player_symbol):
            return 1000
        if game.is_winner(self.opponent_symbol):
            return -1000
        if game.is_full() or depth == 0:
            score = self.heuristic(game, self.player_symbol) - self.heuristic(game, self.opponent_symbol)
            self.seen_states[canonical] = score
            return score

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
            self.seen_states[canonical] = max_eval
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
            self.seen_states[canonical] = min_eval
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
