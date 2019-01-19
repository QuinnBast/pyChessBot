import chess

class Player:
    def __init__(self, color=chess.WHITE):
        self.color = color

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color