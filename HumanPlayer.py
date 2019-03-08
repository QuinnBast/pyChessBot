from Player import Player
import chess

class HumanPlayer (Player):
    def __init__(self):
        super(HumanPlayer, self).__init__()

    def take_turn(self, board):
        invalue = input("Move: ")

        try:
            move = board.parse_san(invalue)
            if move in board.legal_moves:
                board.push(move)
                print("===Your Move===")
        except Exception as e:
            print("Illegal move.")

    def take_two_step_turn(self, board, move):
        try:
            if move in board.legal_moves:
                board.push(move)
                if self.color :
                    print("White player: " + str(move))
                else :
                    print("Black player: " + str(move))
        except Exception as e:
            print("Illegal move.")