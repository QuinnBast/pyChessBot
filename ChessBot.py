import random


class ChessBot:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def take_turn(self, board):
        possible_moves = board.legal_moves

        # enumerate possible moves
        moves = []
        for move in possible_moves:
            moves.append(move)

        # pick a random move from the list and move
        length = len(moves)
        rand_move = random.randint(0, length-1)
        board.push(moves[rand_move])
