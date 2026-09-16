# Morris Game Variant — Board and Game Rules Context

## Board Context

The board contains **23 valid locations**.

Important characteristics of this specific board:

- The four outer corners connect diagonally toward the inner square.
- The left side of the inner square has a line extending outward through its middle point.
- The right side of the inner square has a line extending outward through its middle point.
- The top side of the inner square has a line extending upward through its middle point.
- The **bottom side of the inner square does not have a middle connection downward**.
- The board should be treated exactly as shown in the professor's diagram.
- Do not assume this board has the same connections as standard Nine Men's Morris.

## Board Representation

A board position is represented by **23 locations**.

Each location contains one of:

- `W` — White piece
- `B` — Black piece
- `x` — empty location

Example:

```text
xxxxxBxWWWWWBBBBxxxxxxx
```

The 23 positions correspond to the valid intersections shown on the board.

## Players

The game is played between two players:

- White
- Black

Each player begins with **9 pieces**.

## Goal

The goal is to defeat the opponent by either:

- reducing the opponent to **2 pieces**, or
- blocking the opponent so they have **no legal moves**.

## Game Phases

### Opening

Players take turns placing their pieces on the board.

- Each player has 9 pieces to place.
- One piece is placed per turn.
- A piece may be placed on any vacant board location.

### Midgame

After all pieces have been placed, players move pieces already on the board.

- One piece is moved per turn.
- A piece may move only along a board line to an **adjacent vacant location**.

### Endgame

When a player is reduced to exactly **3 pieces**, that player may hop.

- A piece may move to **any vacant location**.
- The destination does not need to be adjacent.

## Mills

A **mill** is formed when a player has three of their pieces on the same valid straight board line.

When a player forms a mill:

- one opponent piece is removed from the board;
- normally, the removed piece must be an opponent piece that is **not part of a mill**.

The valid mills are determined by the exact lines shown on this specific board.