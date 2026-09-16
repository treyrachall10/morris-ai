def GenerateMovesMidgameEndgame(board):

    if board.count("W") == 3:
        return GenerateHopping(board)

    return GenerateMove(board)


def GenerateMove(board):
    L = []

    for location in range(len(board)):
        if board[location] == "W":

            for j in neighbors(location):
                if board[j] == "x":
                    b = list(board)

                    b[location] = "x"
                    b[j] = "W"

                    b = "".join(b)

                    if closeMill(j, b):
                        GenerateRemove(b, L)
                    else:
                        L.append(b)

    return L


def GenerateHopping(board):
    L = []

    for alpha in range(len(board)):
        if board[alpha] == "W":

            for beta in range(len(board)):
                if board[beta] == "x":
                    b = list(board)

                    b[alpha] = "x"
                    b[beta] = "W"

                    b = "".join(b)

                    if closeMill(beta, b):
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


def neighbors(location):
    neighbor_map = {
        0:  [1, 3, 8],
        1:  [0, 2, 4],
        2:  [1, 5, 13],

        3:  [0, 4, 6, 9],
        4:  [1, 3, 5],
        5:  [2, 4, 7, 12],

        6:  [3, 7, 10],
        7:  [5, 6, 11],

        8:  [0, 9, 20],
        9:  [3, 8, 10, 17],
        10: [6, 9, 14],

        11: [7, 12, 16],
        12: [5, 11, 13, 19],
        13: [2, 12, 22],

        14: [10, 15, 17],
        15: [14, 16, 18],
        16: [11, 15, 19],

        17: [9, 14, 18, 20],
        18: [15, 17, 19, 21],
        19: [12, 16, 18, 22],

        20: [8, 17, 21],
        21: [18, 20, 22],
        22: [13, 19, 21]
    }

    return neighbor_map[location]


def closeMill(location, board):
    color = board[location]

    if color == "x":
        return False

    # Every valid 3-position line on this 23-location board.
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
        (20, 21, 22)
    ]

    for mill in mills:
        if location in mill:
            a, b, c = mill

            if (
                board[a] == color
                and board[b] == color
                and board[c] == color
            ):
                return True

    return False


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

    temp_board = swapColors(board)

    white_moves = GenerateMovesMidgameEndgame(temp_board)

    black_moves = []

    for move in white_moves:
        black_moves.append(swapColors(move))

    return black_moves


def StaticEstimationMidgameEndgame(board):
    numWhitePieces = board.count("W")
    numBlackPieces = board.count("B")

    black_moves = GenerateMovesMidgameEndgameBlack(board)
    numBlackMoves = len(black_moves)

    if numBlackPieces <= 2:
        return 10000

    elif numWhitePieces <= 2:
        return -10000

    elif numBlackMoves == 0:
        return 10000

    else:
        return (
            1000 * (numWhitePieces - numBlackPieces)
            - numBlackMoves
        )


def MiniMax(board, depth, maximizing_player=True):
    # Leaf node
    if depth == 0:
        return StaticEstimationMidgameEndgame(board), board, 1

    positions_evaluated = 0

    # White = MAX
    if maximizing_player:
        possible_moves = GenerateMovesMidgameEndgame(board)

        if len(possible_moves) == 0:
            return StaticEstimationMidgameEndgame(board), board, 1

        best_estimate = float("-inf")
        best_board = None

        for move in possible_moves:
            estimate, _, count = MiniMax(
                move,
                depth - 1,
                False
            )

            positions_evaluated += count

            if estimate > best_estimate:
                best_estimate = estimate
                best_board = move

        return best_estimate, best_board, positions_evaluated

    # Black = MIN
    else:
        possible_moves = GenerateMovesMidgameEndgameBlack(board)

        if len(possible_moves) == 0:
            return StaticEstimationMidgameEndgame(board), board, 1

        best_estimate = float("inf")
        best_board = None

        for move in possible_moves:
            estimate, _, count = MiniMax(
                move,
                depth - 1,
                True
            )

            positions_evaluated += count

            if estimate < best_estimate:
                best_estimate = estimate
                best_board = move

        return best_estimate, best_board, positions_evaluated
