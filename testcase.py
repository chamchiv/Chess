import chess
import chess.engine
import chess.svg
import chessboard

def get_user_move():
    # Prompt the user for a move and return it
    move = input("Enter your move (in algebraic notation): ")
    return chess.Move.from_uci(move)

def get_computer_move(board, engine):
    # Use the Stockfish engine to generate the computer's move
    result = engine.play(board, chess.engine.Limit(time=2.0))
    return result.move

def main():
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("<path_to_stockfish_executable>")

    while not board.is_game_over():
        # Display the chessboard
        print(board)
        svg_board = chess.svg.board(board=board)
        cb = chessboard.Chessboard(svg_board)

        if board.is_checkmate():
            print("Checkmate!")
            break

        if board.is_stalemate():
            print("Stalemate!")
            break

        if board.is_insufficient_material():
            print("Draw due to insufficient material!")
            break

        if board.is_seventyfive_moves():
            print("Draw due to 75-move rule!")
            break

        # Get the user's move
        user_move = get_user_move()
        board.push(user_move)

        if board.is_game_over():
            break

        # Get the computer's move
        computer_move = get_computer_move(board, engine)
        board.push(computer_move)

    print("Game Over")
    print("Result: ", board.result())

    # Close the engine process
    engine.quit()

if __name__ == "__main__":
    main()



 #'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, "K": self.getKingMoves
