from Player import Player
import random


class BotPlayer (Player):
    def __init__(self):
        super(BotPlayer, self).__init__()

    def take_turn(self, board):
        possible_moves = board.legal_moves

        # enumerate possible moves
        moves = []
        for move in possible_moves:
            moves.append(move)

        # pick a random move from the list and move
        length = len(moves)
        if length-1 == 0:
            rand_move = 0
        else:
            rand_move = random.randint(0, length-1)
        board.push(moves[rand_move])