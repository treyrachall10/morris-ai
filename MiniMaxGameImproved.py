MILLS = [
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

NEIGHBORS = [
    [1, 3, 8],          # 0
    [0, 2, 4],          # 1
    [1, 5, 13],         # 2
    [0, 4, 6, 9],       # 3
    [1, 3, 5],          # 4
    [2, 4, 7, 12],      # 5
    [3, 7, 10],         # 6
    [5, 6, 11],         # 7
    [0, 9, 20],         # 8
    [3, 8, 10, 17],     # 9
    [6, 9, 14],         # 10
    [7, 12, 16],        # 11
    [5, 11, 13, 19],    # 12
    [2, 12, 22],        # 13
    [10, 15, 17],       # 14
    [14, 16, 18],       # 15
    [11, 15, 19],       # 16
    [9, 14, 18, 20],    # 17
    [15, 17, 19, 21],   # 18
    [12, 16, 18, 22],   # 19
    [8, 17, 21],        # 20
    [18, 20, 22],       # 21
    [13, 19, 21],       # 22
]


def _count_mills(board, color):
    count = 0
    for a, b, c in MILLS:
        if board[a] == color and board[b] == color and board[c] == color:
            count += 1
    return count


def StaticEstimationMidgameEndgameImproved(board):
    from MiniMaxGame import GenerateMovesMidgameEndgame
    from MiniMaxGameBlack import GenerateMovesMidgameEndgameBlack

    numWhitePieces = board.count("W")
    numBlackPieces = board.count("B")

    numWhiteMoves = len(GenerateMovesMidgameEndgame(board))
    numBlackMoves = len(GenerateMovesMidgameEndgameBlack(board))

    # Terminal win / loss states
    w_loss = (numWhitePieces <= 2 or numWhiteMoves == 0)
    b_loss = (numBlackPieces <= 2 or numBlackMoves == 0)

    if w_loss and b_loss:
        return 0
    if b_loss:
        return 10000
    if w_loss:
        return -10000

    white_mills = 0
    black_mills = 0
    white_threats = 0
    black_threats = 0

    for a, b, c in MILLS:
        p_a, p_b, p_c = board[a], board[b], board[c]
        w_c = (p_a == "W") + (p_b == "W") + (p_c == "W")
        b_c = (p_a == "B") + (p_b == "B") + (p_c == "B")

        if w_c == 3:
            white_mills += 1
        elif b_c == 3:
            black_mills += 1
        elif w_c == 2 and b_c == 0:
            empty = a if p_a == "x" else (b if p_b == "x" else c)
            if numWhitePieces == 3:
                white_threats += 1
            else:
                if any(board[n] == "W" and n != a and n != b for n in NEIGHBORS[empty]):
                    white_threats += 1
        elif b_c == 2 and w_c == 0:
            empty = a if p_a == "x" else (b if p_b == "x" else c)
            if numBlackPieces == 3:
                black_threats += 1
            else:
                if any(board[n] == "B" and n != a and n != b for n in NEIGHBORS[empty]):
                    black_threats += 1

    # Blocked pieces (pieces with no adjacent vacant nodes)
    white_blocked = 0
    black_blocked = 0
    if numWhitePieces > 3:
        for i in range(23):
            if board[i] == "W" and all(board[n] != "x" for n in NEIGHBORS[i]):
                white_blocked += 1
    if numBlackPieces > 3:
        for i in range(23):
            if board[i] == "B" and all(board[n] != "x" for n in NEIGHBORS[i]):
                black_blocked += 1

    return (
        1000 * (numWhitePieces - numBlackPieces)
        + 100 * (white_mills - black_mills)
        + 50 * (white_threats - black_threats)
        + 20 * (numWhiteMoves - numBlackMoves)
        + 30 * (black_blocked - white_blocked)
    )


def MiniMax(board, depth, maximizing_player=True):
    from MiniMaxGame import GenerateMovesMidgameEndgame

    if depth == 0:
        return StaticEstimationMidgameEndgameImproved(board), board, 1

    positions_evaluated = 0

    if maximizing_player:
        possible_moves = GenerateMovesMidgameEndgame(board)

        if len(possible_moves) == 0:
            return StaticEstimationMidgameEndgameImproved(board), board, 1

        best_estimate = float("-inf")
        best_board = None

        for move in possible_moves:
            estimate, _, count = MiniMax(move, depth - 1, False)
            positions_evaluated += count

            if estimate > best_estimate:
                best_estimate = estimate
                best_board = move

        return best_estimate, best_board, positions_evaluated

    from MiniMaxGameBlack import GenerateMovesMidgameEndgameBlack

    possible_moves = GenerateMovesMidgameEndgameBlack(board)

    if len(possible_moves) == 0:
        return StaticEstimationMidgameEndgameImproved(board), board, 1

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
