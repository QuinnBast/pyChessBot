import chess
import chess.svg
from Gui import Gui
import time

class Game:
    def __init__(self, player1, player2):
        self.board = chess.Board()

        player1.set_color(chess.WHITE)
        player2.set_color(chess.BLACK)

        self.player1 = player1
        self.player2 = player2

    def play(self):
        # Start a GUI instance which threads the game
        Gui(self)

    def get_svg(self):
        if len(self.board.move_stack) == 0:
            svg = chess.svg.board(board=self.board)
        else:
            svg = chess.svg.board(board=self.board, lastmove=self.board.move_stack[-1])
        return svg
