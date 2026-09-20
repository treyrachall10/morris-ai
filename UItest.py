import tkinter as tk
from tkinter import ttk, messagebox
import copy

# ---------------------------------------------------------
# 1. 23-LOCATION INDEX MAPPING & GRAPH TOPOLOGY
# ---------------------------------------------------------
# Board positions 0 to 22 according to Morris Variant handout:
# 0:a0,  1:d0,  2:g0
# 3:b1,  4:d1,  5:f1
# 6:c2,  7:e2
# 8:a3,  9:b3, 10:c3, 11:e3, 12:f3, 13:g3
# 14:c4, 15:d4, 16:e4
# 17:b5, 18:d5, 19:f5
# 20:a6, 21:d6, 22:g6

POS_NAMES = [
    "a0", "d0", "g0",
    "b1", "d1", "f1",
    "c2", "e2",
    "a3", "b3", "c3", "e3", "f3", "g3",
    "c4", "d4", "e4",
    "b5", "d5", "f5",
    "a6", "d6", "g6"
]

# Physical UI canvas coordinates (grid 0..6 mapped to canvas pixels)
COORD_GRID = {
    0: (0, 0), 1: (3, 0), 2: (6, 0),
    3: (1, 1), 4: (3, 1), 5: (5, 1),
    6: (2, 2), 7: (4, 2),
    8: (0, 3), 9: (1, 3), 10: (2, 3), 11: (4, 3), 12: (5, 3), 13: (6, 3),
    14: (2, 4), 15: (3, 4), 16: (4, 4),
    17: (1, 5), 18: (3, 5), 19: (5, 5),
    20: (0, 6), 21: (3, 6), 22: (6, 6)
}

# Neighbors list for midgame adjacent movements
NEIGHBORS = {
    0: [1, 3, 8],
    1: [0, 2, 4],
    2: [1, 5, 13],
    3: [0, 4, 6, 9],
    4: [1, 3, 5],
    5: [2, 4, 7, 12],
    6: [3, 7, 10],
    7: [5, 6, 11],
    8: [0, 9, 20],
    9: [3, 8, 10, 17],
    10: [6, 9, 14],
    11: [7, 12, 16],
    12: [5, 11, 13, 19],
    13: [2, 12, 22],
    14: [10, 15],
    15: [14, 16, 18],
    16: [11, 15],
    17: [9, 18, 20],
    18: [15, 17, 19, 21],
    19: [12, 18, 22],
    20: [8, 17, 21],
    21: [18, 20, 22],
    22: [13, 19, 21]
}

# All lines/mills of 3 consecutive points
MILL_TRIPLETS = [
    # Horizontal mills
    (0, 1, 2),
    (3, 4, 5),
    (8, 9, 10),
    (11, 12, 13),
    (14, 15, 16),
    (17, 18, 19),
    (20, 21, 22),
    # Vertical mills
    (0, 8, 20),
    (3, 9, 17),
    (6, 10, 14),
    (1, 4, 15),  # center-bottom line
    (18, 21, 15),  # center-top line connects 15-18-21
    (7, 11, 16),
    (5, 12, 19),
    (2, 13, 22),
    # Diagonals specific to this variant
    (0, 3, 6),
    (2, 5, 7),
    (20, 17, 14),
    (22, 19, 16)
]

# Physical line segments to draw on canvas
LINES = [
    # Outer square
    (0, 1), (1, 2), (2, 13), (13, 22), (22, 21), (21, 20), (20, 8), (8, 0),
    # Middle ring
    (3, 4), (4, 5), (5, 12), (12, 19), (19, 18), (18, 17), (17, 9), (9, 3),
    # Inner lines
    (6, 7), (14, 15), (15, 16), (6, 10), (10, 14), (7, 11), (11, 16),
    # Cross connections
    (8, 9), (9, 10), (11, 12), (12, 13), (1, 4), (18, 21), (15, 18),
    # Diagonal corner connections
    (0, 3), (3, 6), (2, 5), (5, 7), (20, 17), (17, 14), (22, 19), (19, 16)
]


# ---------------------------------------------------------
# 2. GAME LOGIC & MOVE GENERATION
# ---------------------------------------------------------

def close_mill(j, board):
    """Check if piece at index j closes any 3-piece mill."""
    c = board[j]
    if c == 'x':
        return False
    for p1, p2, p3 in MILL_TRIPLETS:
        if j in (p1, p2, p3):
            if board[p1] == c and board[p2] == c and board[p3] == c:
                return True
    return False


def swap_colors(board_str):
    """Swap W <-> B for black move computation."""
    res = []
    for ch in board_str:
        if ch == 'W':
            res.append('B')
        elif ch == 'B':
            res.append('W')
        else:
            res.append('x')
    return "".join(res)


def generate_remove(board_list, L, opp_color='B'):
    """Generate states by removing an opponent piece not in mill."""
    added = False
    for i in range(23):
        if board_list[i] == opp_color:
            if not close_mill(i, board_list):
                b_copy = list(board_list)
                b_copy[i] = 'x'
                L.append("".join(b_copy))
                added = True
    # If all opponent pieces are in mills, any piece can be removed
    if not added:
        for i in range(23):
            if board_list[i] == opp_color:
                b_copy = list(board_list)
                b_copy[i] = 'x'
                L.append("".join(b_copy))


def generate_add(board_str):
    """White placement moves during Opening phase."""
    L = []
    b = list(board_str)
    for i in range(23):
        if b[i] == 'x':
            b_copy = list(b)
            b_copy[i] = 'W'
            if close_mill(i, b_copy):
                generate_remove(b_copy, L, 'B')
            else:
                L.append("".join(b_copy))
    return L


def generate_move(board_str):
    """White regular moves to adjacent vacant intersections."""
    L = []
    b = list(board_str)
    for i in range(23):
        if b[i] == 'W':
            for nbr in NEIGHBORS[i]:
                if b[nbr] == 'x':
                    b_copy = list(b)
                    b_copy[i] = 'x'
                    b_copy[nbr] = 'W'
                    if close_mill(nbr, b_copy):
                        generate_remove(b_copy, L, 'B')
                    else:
                        L.append("".join(b_copy))
    return L


def generate_hopping(board_str):
    """White hopping moves when down to 3 pieces."""
    L = []
    b = list(board_str)
    for i in range(23):
        if b[i] == 'W':
            for j in range(23):
                if b[j] == 'x':
                    b_copy = list(b)
                    b_copy[i] = 'x'
                    b_copy[j] = 'W'
                    if close_mill(j, b_copy):
                        generate_remove(b_copy, L, 'B')
                    else:
                        L.append("".join(b_copy))
    return L


def generate_moves_opening(board_str, player='W'):
    if player == 'W':
        return generate_add(board_str)
    else:
        swapped = swap_colors(board_str)
        moves = generate_add(swapped)
        return [swap_colors(m) for m in moves]


def generate_moves_midgame_endgame(board_str, player='W'):
    if player == 'W':
        w_count = board_str.count('W')
        if w_count == 3:
            return generate_hopping(board_str)
        else:
            return generate_move(board_str)
    else:
        swapped = swap_colors(board_str)
        b_count = swapped.count('W')  # actually Black's piece count
        if b_count == 3:
            moves = generate_hopping(swapped)
        else:
            moves = generate_move(swapped)
        return [swap_colors(m) for m in moves]


def generate_legal_moves(board_str, player, phase):
    if phase == "Opening":
        return generate_moves_opening(board_str, player)
    else:
        return generate_moves_midgame_endgame(board_str, player)


# ---------------------------------------------------------
# 3. STATIC ESTIMATION & MINIMAX AI
# ---------------------------------------------------------

def static_estimation(board_str, phase):
    num_w = board_str.count('W')
    num_b = board_str.count('B')
    if phase == "Opening":
        return num_w - num_b
    else:
        if num_b <= 2:
            return 10000
        elif num_w <= 2:
            return -10000
        black_moves = generate_moves_midgame_endgame(board_str, 'B')
        num_black_moves = len(black_moves)
        if num_black_moves == 0:
            return 10000
        return 1000 * (num_w - num_b) - num_black_moves


def minimax(board_str, depth, is_max, phase, alpha=-1e9, beta=1e9):
    # Base cases
    if depth == 0:
        return static_estimation(board_str, phase), board_str

    player = 'W' if is_max else 'B'
    children = generate_legal_moves(board_str, player, phase)

    if not children:
        # No legal moves available
        return (-10000 if is_max else 10000), board_str

    best_move = children[0]
    if is_max:
        max_eval = -1e9
        for child in children:
            ev, _ = minimax(child, depth - 1, False, phase, alpha, beta)
            if ev > max_eval:
                max_eval = ev
                best_move = child
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 1e9
        for child in children:
            ev, _ = minimax(child, depth - 1, True, phase, alpha, beta)
            if ev < min_eval:
                min_eval = ev
                best_move = child
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval, best_move


# ---------------------------------------------------------
# 4. GUI IMPLEMENTATION
# ---------------------------------------------------------

class MorrisUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Morris Variant - Testing UI & Game Board")
        self.root.geometry("980x750")

        # Game State
        self.board = list("x" * 23)
        self.current_turn = 'W'
        self.ply_count = 0  # 18 moves total in Opening (9 W + 9 B)
        self.phase = "Opening"
        self.ai_color = 'B'  # AI defaults to Black
        self.ai_depth = 2

        # Interactive selection state for canvas clicks
        self.selected_idx = None
        self.pending_remove = False

        self._setup_layout()
        self.render_board()
        self.update_status()

    def _setup_layout(self):
        # Left Panel: Board Canvas
        left_frame = ttk.Frame(self.root, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_size = 560
        self.canvas = tk.Canvas(left_frame, width=self.canvas_size, height=self.canvas_size, bg="#F5F3E9")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Right Panel: Controls & Move String Input
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Game Status Group
        status_box = ttk.LabelFrame(right_frame, text="Game Information", padding=10)
        status_box.pack(fill=tk.X, pady=5)

        self.info_label = ttk.Label(status_box, text="", font=("Helvetica", 11), justify=tk.LEFT)
        self.info_label.pack(anchor=tk.W)

        # String Input Frame
        string_box = ttk.LabelFrame(right_frame, text="Board String Testing / Move Input", padding=10)
        string_box.pack(fill=tk.X, pady=5)

        ttk.Label(string_box, text="Current Board String (23 chars):").pack(anchor=tk.W)
        self.str_entry = ttk.Entry(string_box, font=("Consolas", 11), width=28)
        self.str_entry.pack(fill=tk.X, pady=5)
        self.str_entry.insert(0, "".join(self.board))

        btn_grid = ttk.Frame(string_box)
        btn_grid.pack(fill=tk.X, pady=2)

        ttk.Button(btn_grid, text="Apply String as Move", command=self.apply_move_from_string).pack(side=tk.LEFT,
                                                                                                    expand=True,
                                                                                                    fill=tk.X, padx=2)
        ttk.Button(btn_grid, text="Force Set State", command=self.force_set_state).pack(side=tk.LEFT, expand=True,
                                                                                        fill=tk.X, padx=2)

        # AI & Game Settings
        settings_box = ttk.LabelFrame(right_frame, text="Controls & Opponent", padding=10)
        settings_box.pack(fill=tk.X, pady=5)

        sub_f = ttk.Frame(settings_box)
        sub_f.pack(fill=tk.X, pady=2)
        ttk.Label(sub_f, text="AI Color:").pack(side=tk.LEFT)
        self.ai_color_var = tk.StringVar(value='B')
        ttk.Combobox(sub_f, textvariable=self.ai_color_var, values=['B', 'W', 'None'], state="readonly", width=6).pack(
            side=tk.LEFT, padx=5)

        ttk.Label(sub_f, text="AI Depth:").pack(side=tk.LEFT, padx=(10, 0))
        self.depth_var = tk.IntVar(value=2)
        ttk.Spinbox(sub_f, from_=1, to=6, textvariable=self.depth_var, width=4).pack(side=tk.LEFT, padx=5)

        ctl_btns = ttk.Frame(settings_box)
        ctl_btns.pack(fill=tk.X, pady=5)
        ttk.Button(ctl_btns, text="Trigger AI Move", command=self.trigger_ai_move).pack(side=tk.LEFT, expand=True,
                                                                                        fill=tk.X, padx=2)
        ttk.Button(ctl_btns, text="Reset Game", command=self.reset_game).pack(side=tk.LEFT, expand=True, fill=tk.X,
                                                                              padx=2)

        # Log Window
        log_box = ttk.LabelFrame(right_frame, text="Action Log & Move Validation", padding=10)
        log_box.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = tk.Text(log_box, height=12, width=40, font=("Consolas", 9), state="disabled", wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def update_status(self):
        w_cnt = self.board.count('W')
        b_cnt = self.board.count('B')
        turn_str = "White (W)" if self.current_turn == 'W' else "Black (B)"
        self.info_label.config(
            text=f"Phase: {self.phase}\n"
                 f"Turn: {turn_str}\n"
                 f"White Pieces: {w_cnt} | Black Pieces: {b_cnt}\n"
                 f"Plies Played: {self.ply_count}/18 (Opening)"
        )
        self.str_entry.delete(0, tk.END)
        self.str_entry.insert(0, "".join(self.board))

    # -----------------------------------------------------
    # Canvas Drawing & Coordinate Transform
    # -----------------------------------------------------
    def get_pos(self, idx):
        # Map (0..6, 0..6) to canvas pixel offsets
        gx, gy = COORD_GRID[idx]
        margin = 40
        step = (self.canvas_size - 2 * margin) / 6
        px = margin + gx * step
        py = self.canvas_size - (margin + gy * step)  # Invert y so 0 is bottom
        return px, py

    def render_board(self):
        self.canvas.delete("all")

        # 1. Draw connecting lines
        for u, v in LINES:
            x1, y1 = self.get_pos(u)
            x2, y2 = self.get_pos(v)
            self.canvas.create_line(x1, y1, x2, y2, fill="#555555", width=2)

        # 2. Draw nodes & labels
        r = 16
        for idx in range(23):
            x, y = self.get_pos(idx)
            val = self.board[idx]

            # Circle background color
            fill_col = "#EAEAEA"
            outline_col = "#333333"
            width = 2

            if val == 'W':
                fill_col = "#FFFFFF"
                outline_col = "#111111"
                width = 3
            elif val == 'B':
                fill_col = "#222222"
                outline_col = "#000000"

            # Highlight selected node
            if self.selected_idx == idx:
                outline_col = "#FF9900"
                width = 4

            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_col, outline=outline_col, width=width)

            # Node coordinate label
            lbl_color = "#EEEEEE" if val == 'B' else "#111111"
            self.canvas.create_text(x, y, text=f"{idx}", fill=lbl_color, font=("Helvetica", 9, "bold"))
            self.canvas.create_text(x, y + 23, text=POS_NAMES[idx], fill="#666666", font=("Consolas", 8))

    # -----------------------------------------------------
    # Validation & String Input
    # -----------------------------------------------------
    def apply_move_from_string(self):
        """User tests a move by submitting the 23-char string."""
        new_str = self.str_entry.get().strip()

        # 1. Format checks
        if len(new_str) != 23:
            self.log(f"❌ INVALID FORMAT: String must be 23 characters long (got {len(new_str)}).")
            messagebox.showerror("Invalid Input", f"String length must be 23. Received {len(new_str)}.")
            return

        valid_chars = set("WBx")
        if not set(new_str).issubset(valid_chars):
            self.log("❌ INVALID FORMAT: String must only contain 'W', 'B', and 'x'.")
            messagebox.showerror("Invalid Input", "String can only contain 'W', 'B', and 'x'.")
            return

        # 2. Transition validation against game move generator
        cur_board_str = "".join(self.board)
        legal_next_states = generate_legal_moves(cur_board_str, self.current_turn, self.phase)

        if new_str in legal_next_states:
            self.log(f"✅ LEGAL MOVE accepted for {self.current_turn}: {new_str}")
            self.board = list(new_str)
            self.post_move_step()
        else:
            self.log(f"❌ ILLEGAL MOVE for {self.current_turn} in {self.phase} phase!")
            self.log(f"Target: {new_str}")
            self.log(f"Reason: State cannot be reached by a single legal move from current board.")
            messagebox.showwarning("Illegal Move",
                                   "The submitted board string is NOT a valid legal move for this turn.")

    def force_set_state(self):
        """Overwrites the board directly without move validation."""
        s = self.str_entry.get().strip()
        if len(s) == 23 and set(s).issubset(set("WBx")):
            self.board = list(s)
            self.log(f"⚙️ Board state overridden to: {s}")
            self.render_board()
            self.update_status()
        else:
            messagebox.showerror("Error", "Invalid string format. Must be 23 characters of W, B, x.")

    def post_move_step(self):
        """Handles phase progression, win checks, and AI handoff."""
        self.selected_idx = None
        self.ply_count += 1
        if self.phase == "Opening" and self.ply_count >= 18:
            self.phase = "Midgame/Endgame"
            self.log("🔔 Opening phase completed. Entering Midgame/Endgame phase.")

        # Switch turn
        self.current_turn = 'B' if self.current_turn == 'W' else 'W'
        self.render_board()
        self.update_status()

        # Check win/termination condition
        if self.phase != "Opening":
            cur_pieces = self.board.count(self.current_turn)
            if cur_pieces <= 2:
                winner = 'White' if self.current_turn == 'B' else 'Black'
                self.log(f"🏆 GAME OVER! {winner} wins ({self.current_turn} has only {cur_pieces} pieces)!")
                messagebox.showinfo("Game Over", f"{winner} wins! Opponent reduced to {cur_pieces} pieces.")
                return

            moves = generate_legal_moves("".join(self.board), self.current_turn, self.phase)
            if not moves:
                winner = 'White' if self.current_turn == 'B' else 'Black'
                self.log(f"🏆 GAME OVER! {winner} wins ({self.current_turn} has no legal moves)!")
                messagebox.showinfo("Game Over", f"{winner} wins! Opponent blocked from moving.")
                return

        # Trigger AI if it's the AI's turn
        if self.current_turn == self.ai_color_var.get():
            self.root.after(200, self.trigger_ai_move)

    # -----------------------------------------------------
    # Canvas Click Interaction (Manual Playing)
    # -----------------------------------------------------
    def on_canvas_click(self, event):
        # Locate closest point
        clicked_idx = None
        for idx in range(23):
            px, py = self.get_pos(idx)
            if (event.x - px) ** 2 + (event.y - py) ** 2 <= 20 ** 2:
                clicked_idx = idx
                break

        if clicked_idx is None:
            return

        cur_str = "".join(self.board)
        legal_next_states = generate_legal_moves(cur_str, self.current_turn, self.phase)

        # Case 1: Opening placement
        if self.phase == "Opening":
            if self.board[clicked_idx] != 'x':
                self.log("⚠️ Spot is already occupied.")
                return

            candidate = list(self.board)
            candidate[clicked_idx] = self.current_turn

            if close_mill(clicked_idx, candidate):
                # Mill closed: Prompt user to remove opponent piece
                self.log(
                    f"🔥 Mill closed by {self.current_turn} at {POS_NAMES[clicked_idx]}! Now click an opponent piece to remove.")
                self.board[clicked_idx] = self.current_turn
                self.pending_remove = True
                self.render_board()
            else:
                target_str = "".join(candidate)
                if target_str in legal_next_states:
                    self.board = candidate
                    self.log(f"{self.current_turn} placed at {POS_NAMES[clicked_idx]}")
                    self.post_move_step()

        # Case 2: Mill removal in progress
        elif self.pending_remove:
            opp = 'B' if self.current_turn == 'W' else 'W'
            if self.board[clicked_idx] != opp:
                self.log(f"⚠️ You must select an opponent piece ({opp}) to remove.")
                return

            candidate = list(self.board)
            candidate[clicked_idx] = 'x'
            candidate_str = "".join(candidate)

            # Check if this removal matches any generated legal transition
            if candidate_str in legal_next_states or not close_mill(clicked_idx, self.board):
                self.board = candidate
                self.pending_remove = False
                self.log(f"✂️ Removed opponent piece at {POS_NAMES[clicked_idx]}")
                self.post_move_step()
            else:
                self.log(f"⚠️ Cannot remove {POS_NAMES[clicked_idx]}: piece is part of a mill.")

        # Case 3: Midgame / Endgame movement
        else:
            if self.selected_idx is None:
                if self.board[clicked_idx] == self.current_turn:
                    self.selected_idx = clicked_idx
                    self.render_board()
                else:
                    self.log(f"⚠️ Click your own piece ({self.current_turn}) to move.")
            else:
                src = self.selected_idx
                dst = clicked_idx

                if dst == src:
                    self.selected_idx = None
                    self.render_board()
                    return

                if self.board[dst] != 'x':
                    if self.board[dst] == self.current_turn:
                        self.selected_idx = dst
                        self.render_board()
                    return

                candidate = list(self.board)
                candidate[src] = 'x'
                candidate[dst] = self.current_turn

                if close_mill(dst, candidate):
                    self.board[src] = 'x'
                    self.board[dst] = self.current_turn
                    self.pending_remove = True
                    self.selected_idx = None
                    self.log(f"🔥 Mill formed! Now click an opponent piece to remove.")
                    self.render_board()
                else:
                    target_str = "".join(candidate)
                    if target_str in legal_next_states:
                        self.board = candidate
                        self.log(f"{self.current_turn} moved: {POS_NAMES[src]} -> {POS_NAMES[dst]}")
                        self.post_move_step()
                    else:
                        self.log(f"❌ Move from {POS_NAMES[src]} to {POS_NAMES[dst]} is not legal.")
                        self.selected_idx = None
                        self.render_board()

    # -----------------------------------------------------
    # AI Search Invocation
    # -----------------------------------------------------
    def trigger_ai_move(self):
        depth = self.depth_var.get()
        cur_str = "".join(self.board)
        is_max = (self.current_turn == 'W')

        self.log(f"🤖 AI ({self.current_turn}) thinking (Depth: {depth})...")
        self.root.update()

        est, best_state = minimax(cur_str, depth, is_max, self.phase)

        if best_state == cur_str:
            self.log("🤖 AI has no valid moves!")
            return

        self.log(f"🤖 AI chose move. Estimate: {est}")
        self.log(f"Result State: {best_state}")
        self.board = list(best_state)
        self.post_move_step()

    def reset_game(self):
        self.board = list("x" * 23)
        self.current_turn = 'W'
        self.ply_count = 0
        self.phase = "Opening"
        self.selected_idx = None
        self.pending_remove = False
        self.log("🔄 Game reset.")
        self.render_board()
        self.update_status()


if __name__ == "__main__":
    root = tk.Tk()
    app = MorrisUI(root)
    root.mainloop()