from Player import Player
import random

class BotPlayer (Player):
    def __init__(self):
        super(BotPlayer, self).__init__()
        self.searched_positions = 0

    def take_turn(self, board):
        if board.turn == self.color:
            if board.is_game_over(claim_draw=True):
                return
            else:
                print("=== Bot Move ===")
                # board.push(self.random_move(board))
                # board.push(self.best_material_value(board))
                best_move = self.min_max_tree(2, board)
                print(best_move)
                board.push(best_move)

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
        print("Selected a move from " + str(len(moves)) + " possible moves.")
        return moves[rand_move]

    def best_material_value(self, board):
        # Material value is determined based on the current player's turn of the board state.
        possible_moves = board.legal_moves

        # Determine best material value move
        best_move = None
        best_material_value = -9999
        for move in possible_moves:
            board_copy = board.copy()
            board_copy.push(move)
            # evaluate material value
            value = self.get_material_value(board_copy)
            if value > best_material_value:
                best_move = move
                best_material_value = value
        # Determines the best move based on the current board's player.
        print("Selected a move from " + str(len(possible_moves)) + " possible moves.")
        return best_move

    def min_max_helper(self, depth, board):
        if depth == 0:
            self.searched_positions = self.searched_positions + 1
            # Return the board state and the board's material value
            return board, self.get_material_value(board)

        possible_moves = board.legal_moves

        if board.turn == self.color:
            # We want to maximize the heuristic
            best_board = None
            best_value = -9999
            for move in possible_moves:
                # Generate a new board
                board_copy = board.copy()
                board_copy.push(move)

                # Recursion
                possible_board, possible_board_value = self.min_max_helper(depth - 1, board_copy)

                if possible_board_value > best_value:
                    best_value = self.get_material_value(board_copy)
                    best_board = board_copy

            return best_board, best_value
        else:
            # We want to minimize the heuristic (assume opponent will make the best move)
            best_board = None
            best_value = 9999

            for move in possible_moves:
                # Generate a new board
                board_copy = board.copy()
                board_copy.push(move)

                # Recursion
                possible_board, possible_board_value = self.min_max_helper(depth - 1, board_copy)

                # Minimize our own position on an opponent's move
                if possible_board_value < best_value:
                    best_value = self.get_material_value(board_copy)
                    best_board = board_copy

            return best_board, best_value

    def min_max_tree(self, depth, board):
        move = self.min_max_helper(depth, board)[0].pop()
        print("Selected a move from " + str(self.searched_positions) + " possible moves at a depth of " + str(depth))
        self.searched_positions = 0
        return move

    def get_material_value(self, board):
        # Determine the material value of the board
        pieces = board.piece_map()

        total_piece_value = 0

        for p in pieces:
            piece_value = 1 if pieces[p].color != board.turn else -1
            symbol = pieces[p].symbol().lower()
            if (symbol == 'p'):
                piece_value = piece_value * 10
            elif (symbol == 'b' or symbol == 'n'):
                piece_value = piece_value * 30
            elif (symbol == 'r'):
                piece_value = piece_value * 50
            elif (symbol == 'q'):
                piece_value = piece_value * 90
            elif (symbol == 'k'):
                piece_value = piece_value * 1000
            total_piece_value = total_piece_value + piece_value

        return total_piece_value
