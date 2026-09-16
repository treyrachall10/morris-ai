def AlphaBeta(board, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
    from MiniMaxOpening import GenerateMovesOpening, StaticEstimationOpening

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
            estimate, _, count = AlphaBeta(move, depth - 1, alpha, beta, False)
            positions_evaluated += count

            if estimate > best_estimate:
                best_estimate = estimate
                best_board = move

            if best_estimate > alpha:
                alpha = best_estimate

            if alpha >= beta:
                break

        return best_estimate, best_board, positions_evaluated

    from MiniMaxOpeningBlack import GenerateMovesOpeningBlack

    possible_moves = GenerateMovesOpeningBlack(board)

    if len(possible_moves) == 0:
        return StaticEstimationOpening(board), board, 1

    best_estimate = float("inf")
    best_board = None

    for move in possible_moves:
        estimate, _, count = AlphaBeta(move, depth - 1, alpha, beta, True)
        positions_evaluated += count

        if estimate < best_estimate:
            best_estimate = estimate
            best_board = move

        if best_estimate < beta:
            beta = best_estimate

        if alpha >= beta:
            break

    return best_estimate, best_board, positions_evaluated


if __name__ == "__main__":
    import sys

    input_file, output_file, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])

    with open(input_file) as f:
        board = f.read().strip()

    estimate, best_board, positions = AlphaBeta(board, depth)

    with open(output_file, "w") as f:
        f.write(best_board)

    print("Board Position: " + best_board)
    print("Positions evaluated by static estimation: " + str(positions))
    print("MINIMAX estimate: " + str(estimate))
