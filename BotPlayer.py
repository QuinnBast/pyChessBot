from Player import Player
import random

class BotPlayer (Player):
    def __init__(self):
        super(BotPlayer, self).__init__()

    def take_turn(self, board):
        if board.is_game_over(claim_draw=True):
            return
        else:
            self.best_material_value(board)

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
        board.push(moves[rand_move])

    def best_material_value(self, board):

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
        board.push(best_move)

    def get_material_value(self, board):
        # Determine the material value of the board
        pieces = board.piece_map()

        total_piece_value = 0

        for p in pieces:
            piece_value = 1
            if (pieces[p].color != self.color):
                piece_value = -1
            symbol = pieces[p].symbol().lower()
            if (symbol == 'p'):
                piece_value = piece_value * 10
            elif (symbol == 'b' or symbol == 'n'):
                piece_value = piece_value * 30
            elif (symbol == 'r'):
                piece_value = piece_value * 50
            elif (symbol == 'q'):
                piece_value = piece_value * 80
            elif (symbol == 'k'):
                piece_value = piece_value * 1000
            total_piece_value = total_piece_value + piece_value

        return total_piece_value
