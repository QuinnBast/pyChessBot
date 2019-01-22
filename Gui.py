import sys
from PyQt4 import QtGui, QtSvg
from PyQt4.QtCore import QByteArray, QThread, pyqtSignal, QEvent, QObject, QCoreApplication
from PyQt4.QtGui import QApplication
import time
from HumanPlayer import HumanPlayer
import chess
import math

WIDTH = 1024
HEIGHT = 1024

class ClickFilter (QObject):
    clicked = pyqtSignal(object)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease:
            self.clicked.emit(event)
            return True
        return False

class Gui:

    app = QtGui.QApplication(sys.argv)
    svgWidget = QtSvg.QSvgWidget()

    def __init__(self, game):
        app = QtGui.QApplication(sys.argv)

        gameThread = GameThread(game) # Starts the game in a thread
        gameThread.svg.connect(self.on_data_ready)
        gameThread.is_over.connect(self.quit)
        gameThread.start()

        filter = ClickFilter()
        filter.clicked.connect(gameThread.click)

        self.svgWidget.installEventFilter(filter)

        app.exec_()

    def quit(self, data):
        print("Checkmate")
        #if data:
            #quit()

    def on_data_ready(self, data):
        self.svgWidget.renderer().load(QByteArray(data))
        self.svgWidget.setFixedSize(WIDTH, HEIGHT)
        self.svgWidget.show()


class GameThread(QThread):

    svg = pyqtSignal(object)
    is_over = pyqtSignal(object)
    do_turn = pyqtSignal(object)
    waiting = True
    waiting_player = True
    first_square = None
    second_square = None

    def __init__(self, game):
        super(GameThread, self).__init__()
        self.game = game
        self.board = game.board
        self.player1 = game.player1
        self.player2 = game.player2
        self.squares = None

    def run(self):
        while not self.board.is_game_over(claim_draw=True):
            self.svg.emit(self.game.get_svg(self.squares))
            # Refresh the screen 60 times per second
            time.sleep(1/3)

            if self.board.turn == self.player1.get_color():
                if isinstance(self.player1, HumanPlayer):
                    self.waiting = True
                    if self.waiting:
                        QCoreApplication.processEvents()
                else:
                    self.player1.take_turn(self.board)
            else:
                if isinstance(self.player2, HumanPlayer):
                    self.waiting = True
                    if self.waiting:
                        QCoreApplication.processEvents()
                else:
                    self.player2.take_turn(self.board)

        # Emit game over
        QCoreApplication.processEvents()
        self.svg.emit(self.game.get_svg(self.squares))
        self.is_over.emit(True)

    def click(self, event):
        # If the game is waiting for the user's turn, process their mouse click.
        if self.waiting:

            # determine click location
            border_size = (20 / 400) * WIDTH
            board_x = event.x() - border_size
            board_y = event.y() - border_size

            square_size = (45 / 400) * WIDTH

            clicked_file = int(math.floor(board_x / square_size))
            clicked_rank = int(math.floor(8 - (board_y / square_size)))

            clicked_square = chess.square(clicked_file, clicked_rank)

            if self.first_square is None:
                self.first_square = clicked_square

                self.squares = self.game.get_moves_from_square(self.first_square)
            else:
                self.second_square = clicked_square
                self.squares = None

                # player take turn.
                if self.board.turn == self.player1.get_color():
                    self.player1.take_two_step_turn(self.board, self.first_square, self.second_square)
                else:
                    self.player2.take_two_step_turn(self.board, self.first_square, self.second_square)

                self.waiting = False
                self.first_square = None
                self.second_square = None
