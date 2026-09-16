def GenerateMovesOpening(board):
    return GenerateAdd(board)


def GenerateAdd(board):
    L = []

    for location in range(len(board)):
        if board[location] == "x":
            b = list(board)
            b[location] = "W"
            b = "".join(b)

            if closeMill(location, b):
                GenerateRemove(b, L)
            else:
                L.append(b)

    return L


def GenerateRemove(board, L):
    added_position = False

    for location in range(len(board)):
        if board[location] == "B":
            if not closeMill(location, board):
                b = list(board)
                b[location] = "x"
                L.append("".join(b))
                added_position = True

    if not added_position:
        L.append(board)


def closeMill(location, board):
    color = board[location]

    if color == "x":
        return False

    mills = [
        (0, 1, 2),
        (0, 3, 6),
        (0, 8, 20),
        (2, 5, 7),
        (2, 13, 22),
        (3, 4, 5),
        (3, 9, 17),
        (5, 12, 19),
        (6, 10, 14),
        (7, 11, 16),
        (8, 9, 10),
        (11, 12, 13),
        (14, 15, 16),
        (14, 17, 20),
        (15, 18, 21),
        (16, 19, 22),
        (17, 18, 19),
        (20, 21, 22),
    ]

    for mill in mills:
        if location in mill:
            a, b, c = mill
            if board[a] == color and board[b] == color and board[c] == color:
                return True

    return False


def StaticEstimationOpening(board):
    numWhitePieces = board.count("W")
    numBlackPieces = board.count("B")
    return numWhitePieces - numBlackPieces


def MiniMax(board, depth, maximizing_player=True):
    if depth == 0:
        return StaticEstimationOpening(board), board, 1

    positions_evaluated = 0

    if maximizing_player:
        possible_moves = GenerateMovesOpening(board)

        if len(possible_moves) == 0:
            return StaticEstimationOpening(board), board, 1

        best_estimate = float("-inf")
        best_board = None

        for move in possible_moves:
            estimate, _, count = MiniMax(move, depth - 1, False)
            positions_evaluated += count

            if estimate > best_estimate:
                best_estimate = estimate
                best_board = move

        return best_estimate, best_board, positions_evaluated

    from MiniMaxOpeningBlack import GenerateMovesOpeningBlack

    possible_moves = GenerateMovesOpeningBlack(board)

    if len(possible_moves) == 0:
        return StaticEstimationOpening(board), board, 1

    best_estimate = float("inf")
    best_board = None

    for move in possible_moves:
        estimate, _, count = MiniMax(move, depth - 1, True)
        positions_evaluated += count

        if estimate < best_estimate:
            best_estimate = estimate
            best_board = move

    return best_estimate, best_board, positions_evaluated


if __name__ == "__main__":
    import sys

    input_file, output_file, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])

    with open(input_file) as f:
        board = f.read().strip()

    estimate, best_board, positions = MiniMax(board, depth, True)

    with open(output_file, "w") as f:
        f.write(best_board)

    print("Board Position: " + best_board)
    print("Positions evaluated by static estimation: " + str(positions))
    print("MINIMAX estimate: " + str(estimate))
