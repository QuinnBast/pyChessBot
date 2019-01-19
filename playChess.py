from Game import Game
from BotPlayer import BotPlayer
from HumanPlayer import HumanPlayer

# Create a new game with two bots and play the game
game = Game(BotPlayer(), HumanPlayer())
game.play()
