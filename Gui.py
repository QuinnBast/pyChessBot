import sys
from PyQt4 import QtGui, QtSvg
from PyQt4.QtCore import QByteArray, QThread, pyqtSignal, QEvent, QObject, QCoreApplication
from PyQt4.QtGui import QApplication
import time
from HumanPlayer import HumanPlayer
import chess
import math

WIDTH = 480
HEIGHT = 480

class ClickFilter (QObject):
    clicked = pyqtSignal(object)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease:
            self.clicked.emit(event)
            return True
        return False

class Gui:

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
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

        # Create main menu
        mainMenu = self.window.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')
        p1Menu = mainMenu.addMenu('Player 1')
        p2Menu = mainMenu.addMenu('Player 2')

        # Add exit button
        newGameButton = QtGui.QAction('New Game', self.window)
        newGameButton.setShortcut('Ctrl+N')
        newGameButton.setStatusTip('New Game')
        newGameButton.triggered.connect(game.newgame)
        fileMenu.addAction(newGameButton)

        p1HumanButton = QtGui.QAction('Human Player', self.window)
        p1HumanButton.triggered.connect(lambda: game.setPlayer(1, "Human") and game.newgame())
        p1Menu.addAction(p1HumanButton)

        p1BotRandButton = QtGui.QAction('Beginner (Random Bot)', self.window)
        p1BotRandButton.triggered.connect(lambda: game.setPlayer(1, "BotRand") and game.newgame())
        p1Menu.addAction(p1BotRandButton)

        p1BotMaterialButton = QtGui.QAction('Easy (Material Value Bot)', self.window)
        p1BotMaterialButton.triggered.connect(lambda: game.setPlayer(1, "BotMaterial") and game.newgame())
        p1Menu.addAction(p1BotMaterialButton)

        p1BotMiniMaxButton = QtGui.QAction('Medium (MiniMax Bot)', self.window)
        p1BotMiniMaxButton.triggered.connect(lambda: game.setPlayer(1, "BotMinimax") and game.newgame())
        p1Menu.addAction(p1BotMiniMaxButton)

        p1BotAlphaBetaButton = QtGui.QAction('Hard (AlphaBeta Bot)', self.window)
        p1BotAlphaBetaButton.triggered.connect(lambda: game.setPlayer(1, "BotAlphaBeta") and game.newgame())
        p1Menu.addAction(p1BotAlphaBetaButton)



        p2HumanButton = QtGui.QAction('Human Player', self.window)
        p2HumanButton.triggered.connect(lambda: game.setPlayer(2, "Human") and game.newgame())
        p2Menu.addAction(p2HumanButton)

        p2BotRandButton = QtGui.QAction('Beginner (Random Bot)', self.window)
        p2BotRandButton.triggered.connect(lambda: game.setPlayer(2, "BotRand") and game.newgame())
        p2Menu.addAction(p2BotRandButton)

        p2BotMaterialButton = QtGui.QAction('Easy (Material Value Bot)', self.window)
        p2BotMaterialButton.triggered.connect(lambda: game.setPlayer(2, "BotMaterial") and game.newgame())
        p2Menu.addAction(p2BotMaterialButton)

        p2BotMiniMaxButton = QtGui.QAction('Medium (MiniMax Bot)', self.window)
        p2BotMiniMaxButton.triggered.connect(lambda: game.setPlayer(2, "BotMinimax") and game.newgame())
        p2Menu.addAction(p2BotMiniMaxButton)

        p2BotAlphaBetaButton = QtGui.QAction('Hard (AlphaBeta Bot)', self.window)
        p2BotAlphaBetaButton.triggered.connect(lambda: game.setPlayer(2, "BotAlphaBeta") and game.newgame())
        p2Menu.addAction(p2BotAlphaBetaButton)



        self.window.show()
        self.window.setCentralWidget(self.svgWidget)

        app.exec_()

    def quit(self, data):
        print("Checkmate")
        #if data:
            #quit()

    def on_data_ready(self, data):
        self.svgWidget.renderer().load(QByteArray(data))
        self.svgWidget.setFixedSize(WIDTH, HEIGHT)
        #self.svgWidget.show()


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
        self.squares = None
        self.gameOver = False

    def run(self):
        while True:
            if not self.game.get_game().is_game_over(claim_draw=True):
                self.gameOver = False
                self.svg.emit(self.game.get_svg(self.squares))
                # Refresh the screen 60 times per second
                time.sleep(1/3)

                board = self.game.get_game()
                player1 = self.game.get_player1()
                player2 = self.game.get_player2()

                if board.turn == player1.get_color():
                    if isinstance(player1, HumanPlayer):
                        self.waiting = True
                        if self.waiting:
                            QCoreApplication.processEvents()
                    else:
                        player1.take_turn(board)
                else:
                    if isinstance(player2, HumanPlayer):
                        self.waiting = True
                        if self.waiting:
                            QCoreApplication.processEvents()
                    else:
                        player2.take_turn(board)
            else:
                if self.gameOver == False:
                    print("Game over")
                    self.gameOver = True

        # # Emit game over
        # QCoreApplication.processEvents()
        # self.svg.emit(self.game.get_svg(self.squares))
        # self.is_over.emit(True)

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

                board = self.game.get_game()
                player1 = self.game.get_player1()
                player2 = self.game.get_player2()

                # Determine if the move is a promotion
                if board.turn == player1.get_color():
                    # Determine if the move is a promotion move
                    if clicked_rank == 7 and board.piece_at(self.first_square).piece_type == chess.PAWN:
                        promote_to = input("Promote pawn to (b, n, r, q): ")
                        if promote_to == 'b':
                            move = chess.Move(self.first_square, self.second_square, chess.BISHOP)
                        elif promote_to == 'n':
                            move = chess.Move(self.first_square, self.second_square, chess.KNIGHT)
                        elif promote_to == 'r':
                            move = chess.Move(self.first_square, self.second_square, chess.ROOK)
                        elif promote_to == 'q':
                            move = chess.Move(self.first_square, self.second_square, chess.QUEEN)
                    else:
                        move = chess.Move(self.first_square, self.second_square)

                elif board.turn == player2.get_color():
                    # Determine if the move is a promotion move
                    if clicked_rank == 0 and board.piece_at(self.first_square).piece_type == chess.PAWN:
                        promote_to = input("Promote pawn to (b, n, r, q): ")
                        if promote_to == 'b':
                            move = chess.Move(self.first_square, self.second_square, chess.BISHOP)
                        elif promote_to == 'n':
                            move = chess.Move(self.first_square, self.second_square, chess.KNIGHT)
                        elif promote_to == 'r':
                            move = chess.Move(self.first_square, self.second_square, chess.ROOK)
                        elif promote_to == 'q':
                            move = chess.Move(self.first_square, self.second_square, chess.QUEEN)
                    else:
                        move = chess.Move(self.first_square, self.second_square)

                # player take turn.
                if board.turn == player1.get_color():
                    player1.take_two_step_turn(board, move)
                else:
                    player2.take_two_step_turn(board, move)

                self.waiting = False
                self.first_square = None
                self.second_square = None
