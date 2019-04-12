from Player import Player
import random

class BotPlayer (Player):
    def __init__(self, difficulty):
        super(BotPlayer, self).__init__()
        self.searched_positions = 0
        self.difficulty = difficulty

    def take_turn(self, board):
        if board.turn == self.color:
            if board.is_game_over(claim_draw=True):
                return
            else:
                if self.difficulty == "rand":
                    best_move = self.random_move(board)
                elif self.difficulty == "material":
                    best_move = self.best_material_value(board)
                elif self.difficulty == "minimax":
                    best_move = self.min_max(3, board)
                elif self.difficulty == "alphabeta":
                    best_move = self.alpha_beta(3, board)

                print(best_move)
                board.push(best_move)

                print("Selected a move from " + str(self.searched_positions) + " possible moves.")
                if self.color:
                    print("White bot: " + str(best_move))
                else:
                    print("Black bot: " + str(best_move))
                self.searched_positions = 0

    def random_move(self, board):
        possible_moves = board.legal_moves

        # enumerate possible moves
        moves = []
        for move in possible_moves:
            moves.append(move)

        # pick a random move from the list and move
        length = len(moves)
        if length - 1 == 0:
            rand_move = 0
        else:
            rand_move = random.randint(0, length - 1)

        self.searched_positions = len(moves)
        return moves[rand_move]

    def best_material_value(self, board):
        # Material value is determined based on the current player's turn of the board state.
        possible_moves = board.legal_moves
        moves = 0

        # Determine best material value move
        best_move = None
        best_material_value = -9999
        for move in possible_moves:
            moves = moves + 1
            board_copy = board.copy()
            board_copy.push(move)
            # evaluate material value
            value = self.get_material_value(board_copy)
            if value > best_material_value:
                best_move = move
                best_material_value = value
        # Determines the best move based on the current board's player.
        self.searched_positions = moves
        return best_move

    def min_max_helper(self, depth, board):
        # Base case, at max depth return the board and it's position.
        if depth == 0:
            self.searched_positions = self.searched_positions + 1
            # Return the board state and the board's material value
            return self.get_material_value(board)

        possible_moves = board.legal_moves

        if board.turn == self.color:
            # We want to maximize the heuristic
            best_value = -9999
            for move in possible_moves:
                # Generate a new board
                board_copy = board.copy()
                board_copy.push(move)

                # Recursion determines the net layer's min or max value of the next depth
                # Or, if at the last depth, returns the next board state's values
                best_value = max(best_value, self.min_max_helper(depth - 1, board_copy))

            # Return the board's max value at this layer.
            return best_value
        else:
            # We want to minimize the heuristic (assume opponent will make the best move)
            worst_value = 9999

            for move in possible_moves:
                # Generate a new board
                board_copy = board.copy()
                board_copy.push(move)

                # Recursion to determine the next layer's max value.
                worst_value = min(worst_value, self.min_max_helper(depth - 1, board_copy))

            return worst_value

    def min_max_root(self, depth, board):
        possible_moves = board.legal_moves
        best_value = -9999
        best_board = None
        for move in possible_moves:
            # Generate a new board
            board_copy = board.copy()
            board_copy.push(move)

            if best_board is None:
                best_board = board_copy

            value = self.min_max_helper(depth - 1, board_copy)

            if value > best_value:
                best_board = board_copy
                best_value = value

        return best_board

    def min_max(self, depth, board):
        move = self.min_max_root(depth, board).pop()
        return move

    def alpha_beta(self, depth, board):
        move = self.alpha_beta_root(depth, board).pop()
        return move

    def alpha_beta_root(self, depth, board):
        possible_moves = board.legal_moves
        best_value = -9999
        best_board = None
        for move in possible_moves:
            # Generate a new board
            board_copy = board.copy()
            board_copy.push(move)

            if best_board is None:
                best_board = board_copy

            value = self.alpha_beta_helper(depth - 1, board_copy, -999999, 999999)

            if value > best_value:
                best_board = board_copy
                best_value = value

        return best_board

    def alpha_beta_helper(self, depth, board, alpha, beta):
        # Base case, at max depth return the board and it's position.
        if depth == 0:
            self.searched_positions = self.searched_positions + 1
            # Return the board state and the board's material value
            return self.get_material_value(board)

        possible_moves = board.legal_moves

        if board.turn == self.color:
            # We want to maximize the heuristic
            best_value = -999999
            for move in possible_moves:
                # Generate a new board
                board_copy = board.copy()
                board_copy.push(move)

                # Recursion determines the net layer's min or max value of the next depth
                # Or, if at the last depth, returns the next board state's values
                best_value = max(best_value, self.alpha_beta_helper(depth - 1, board_copy, alpha, beta))
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    return best_value

            # Return the board's max value at this layer.
            return best_value
        else:
            # We want to minimize the heuristic (assume opponent will make the best move)
            worst_value = 999999

            for move in possible_moves:
                # Generate a new board
                board_copy = board.copy()
                board_copy.push(move)

                # Recursion to determine the next layer's max value.
                worst_value = min(worst_value, self.alpha_beta_helper(depth - 1, board_copy, alpha, beta))
                beta = min(beta, worst_value)

                if beta <= alpha:
                    return worst_value

            return worst_value

    def get_material_value(self, board):
        # Determine the material value of the board
        pieces = board.piece_map()

        total_piece_value = 0

        for p in pieces:
            # Your color = positive, enemey = negative
            piece_value = 1 if pieces[p].color != board.turn else -1
            symbol = pieces[p].symbol().lower()
            if (symbol == 'p'): # Pawn value
                piece_value = piece_value * 10
            elif (symbol == 'b' or symbol == 'n'): # Bishop and Knight
                piece_value = piece_value * 30
            elif (symbol == 'r'): # Rook
                piece_value = piece_value * 50
            elif (symbol == 'q'): # Queen
                piece_value = piece_value * 90
            elif (symbol == 'k'): # King
                piece_value = piece_value * 1000
            total_piece_value = total_piece_value + piece_value

        if board.is_checkmate():
            total_piece_value += - 1000

        return total_piece_value
