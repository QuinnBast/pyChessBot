import chess
import chess.svg
from Gui import Gui
import time
from HumanPlayer import HumanPlayer
from BotPlayer import BotPlayer
from Stockfish import Stockfish

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

    def get_svg(self, squareList):
        if len(self.board.move_stack) == 0:
            svg = chess.svg.board(board=self.board, squares=squareList)
        else:
            svg = chess.svg.board(board=self.board, lastmove=self.board.move_stack[-1], squares=squareList)
        return svg

    def get_moves_from_square(self, square):
        square_moves = chess.SquareSet()
        for move in self.board.legal_moves:
            if move.from_square == square:
                square_moves.add(move.to_square)
        if len(square_moves.tolist()) == 0:
            return None
        else:
            return square_moves

    def newgame(self):
        self.board.reset()

    def setPlayer(self, playerNumber, playerType):
        if playerNumber == 1:
            if playerType == "Human":
                self.player1 = HumanPlayer()
            elif playerType == "BotRand":
                self.player1 = BotPlayer("rand")
            elif playerType == "BotMaterial":
                self.player1 = BotPlayer("material")
            elif playerType == "BotMinimax":
                self.player1 = BotPlayer("minimax")
            elif playerType == "BotAlphaBeta":
                self.player1 = BotPlayer("alphabeta")
            self.player1.set_color(chess.WHITE)
        else:
            if playerType == "Human":
                self.player2 = HumanPlayer()
            elif playerType == "BotRand":
                self.player2 = BotPlayer("rand")
            elif playerType == "BotMaterial":
                self.player2 = BotPlayer("material")
            elif playerType == "BotMinimax":
                self.player2 = BotPlayer("minimax")
            elif playerType == "BotAlphaBeta":
                self.player2 = BotPlayer("alphabeta")
            self.player2.set_color(chess.BLACK)

        return True

    def get_game(self):
        return self.board

    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

