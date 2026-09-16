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


def _count_mills(board, color):
    count = 0
    for a, b, c in MILLS:
        if board[a] == color and board[b] == color and board[c] == color:
            count += 1
    return count


def StaticEstimationMidgameEndgameImproved(board):
    pass


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
