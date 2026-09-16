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
        (3, 4, 5),
        (8, 9, 10),
        (11, 12, 13),
        (14, 15, 16),
        (17, 18, 19),
        (20, 21, 22),

        (0, 3, 6),
        (0, 8, 20),
        (2, 5, 7),
        (2, 13, 22),

        (3, 9, 17),
        (5, 12, 19),

        (6, 10, 14),
        (7, 11, 16),

        (14, 17, 20),
        (15, 18, 21),
        (16, 19, 22)
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


def StaticEstimationOpening(board):
    numWhitePieces = board.count("W")
    numBlackPieces = board.count("B")

    return numWhitePieces - numBlackPieces


def MiniMax():
    pass