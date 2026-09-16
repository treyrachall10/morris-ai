def swapColors(board):
    swapped = []

    for piece in board:
        if piece == "W":
            swapped.append("B")
        elif piece == "B":
            swapped.append("W")
        else:
            swapped.append("x")

    return "".join(swapped)


def GenerateMovesMidgameEndgameBlack(board):
    from MiniMaxGame import GenerateMovesMidgameEndgame

    tempb = swapColors(board)
    white_moves = GenerateMovesMidgameEndgame(tempb)
    return [swapColors(move) for move in white_moves]


def MiniMax(board, depth, maximizing_player=False):
    from MiniMaxGame import MiniMax as WhiteMiniMax

    return WhiteMiniMax(board, depth, maximizing_player)


if __name__ == "__main__":
    import sys

    input_file, output_file, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])

    with open(input_file) as f:
        board = f.read().strip()

    estimate, best_board, positions = MiniMax(board, depth, False)

    with open(output_file, "w") as f:
        f.write(best_board)

    print("Board Position: " + best_board)
    print("Positions evaluated by static estimation: " + str(positions))
    print("MINIMAX estimate: " + str(estimate))
