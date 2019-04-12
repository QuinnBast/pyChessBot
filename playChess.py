from Game import Game
from BotPlayer import BotPlayer
from HumanPlayer import HumanPlayer
from Stockfish import Stockfish

# Create a new game with two bots and play the game
game = Game(HumanPlayer(), BotPlayer("rand"))
game.play()
