import chess.uci
from Player import Player

class Stockfish (Player):
    location = "stockfish-10-win\stockfish-10-win\Windows\stockfish_10_x64.exe"

    def __init__(self):
        super(Stockfish, self).__init__()
        self.engine = chess.uci.popen_engine(self.location)
        self.engine.uci()
        self.engine.ucinewgame()
        print(self.engine.name)

    def get_color(self):
        return self.color

    def take_turn(self, board):
        self.engine.position(board)
        async = self.engine.go(searchmoves=board.legal_moves, depth=1, mate=2,
                               infinite=False, async_callback=True)

        while not async.done():
            pass

        response = async.result()
        print(response)
        if response is not None:
            board.push(response[0])
        else:
            board.push(response[1])

