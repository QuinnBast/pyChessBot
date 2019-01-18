import chess
from ChessBot import ChessBot
import copy

# Create a new game
board = chess.Board()

color = None

while color is None:
    color = input("Choose your color: ")
    if str(color).lower() == "white":
        color = chess.WHITE
    else:
        color = chess.BLACK


bot = ChessBot(not color)
game_over = False

while not game_over:
    print(board)
    if board.turn == bot.get_color():
        bot.take_turn(board)
        print("===Bot Move===")
    else:
        invalue = input("Move: ")
        if invalue == "ff":
            game_over = True
            continue
        try:
            move = board.parse_san(invalue)
            if move in board.legal_moves:
                board.push(move)
            print("===Your Move===")
        except Exception as e:
            print("Illegal move.")
    game_over = board.is_checkmate()

# Assign the bot a color
print("Game over.")
print(board)

# Need to deep copy otherwise the stack variable is just a reference and will reset after board reset
stack = copy.deepcopy(board.move_stack)
# Need to reset the board to get the variation_san move list
board.reset()
print(board.variation_san(stack))