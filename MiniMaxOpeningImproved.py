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


def StaticEstimationOpeningImproved(board):
    numWhitePieces = board.count("W")
    numBlackPieces = board.count("B")

    white_mills = 0
    black_mills = 0
    white_two_piece = 0
    black_two_piece = 0
    white_fork_cand = [0] * 23
    black_fork_cand = [0] * 23

    for a, b, c in MILLS:
        p_a, p_b, p_c = board[a], board[b], board[c]
        w_c = (p_a == "W") + (p_b == "W") + (p_c == "W")
        b_c = (p_a == "B") + (p_b == "B") + (p_c == "B")

        if w_c == 3:
            white_mills += 1
        elif b_c == 3:
            black_mills += 1
        elif w_c == 2 and b_c == 0:
            white_two_piece += 1
            empty = a if p_a == "x" else (b if p_b == "x" else c)
            white_fork_cand[empty] += 1
        elif b_c == 2 and w_c == 0:
            black_two_piece += 1
            empty = a if p_a == "x" else (b if p_b == "x" else c)
            black_fork_cand[empty] += 1

    white_forks = sum(1 for cnt in white_fork_cand if cnt >= 2)
    black_forks = sum(1 for cnt in black_fork_cand if cnt >= 2)

    white_mobility = 0
    black_mobility = 0
    for i in range(23):
        piece = board[i]
        if piece == "W":
            white_mobility += sum(1 for n in NEIGHBORS[i] if board[n] == "x")
        elif piece == "B":
            black_mobility += sum(1 for n in NEIGHBORS[i] if board[n] == "x")

    return (
        1000 * (numWhitePieces - numBlackPieces)
        + 100 * (white_mills - black_mills)
        + 40 * (white_two_piece - black_two_piece)
        + 130 * (white_forks - black_forks)
        + 10 * (white_mobility - black_mobility)
    )


def MiniMax(board, depth, maximizing_player=True):
    from MiniMaxOpening import GenerateMovesOpening

    if depth == 0:
        return StaticEstimationOpeningImproved(board), board, 1

    positions_evaluated = 0

    if maximizing_player:
        possible_moves = GenerateMovesOpening(board)

        if len(possible_moves) == 0:
            return StaticEstimationOpeningImproved(board), board, 1

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
        return StaticEstimationOpeningImproved(board), board, 1

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
