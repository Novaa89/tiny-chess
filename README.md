# tiny-chess

A strong chess engine in **4,025 bytes** of pure Python — an entry for the make.fun **tiny-chess-01** bounty (strongest chess engine in 4KB of Python).

## Running

The engine speaks UCI over stdin/stdout:

```bash
python3 engine.py
```

Supported commands: `uci`, `isready`, `ucinewgame`, `position startpos|fen ... [moves ...]`, `go depth N`, `go movetime <ms>`, `stop`, `quit`.

## Design

- 120-square mailbox board in a `bytearray`
- Pseudo-legal move generation (castling, en passant, all promotions) with legality enforced by a capture-based attack test
- Negamax search with alpha-beta pruning, quiescence search on captures/promotions, iterative deepening, MVV-LVA move ordering, mate-distance scoring
- Evaluation: material + piece-square tables

Legality verified against published perft counts (start position, Kiwipete, en-passant pin, promotion/castling positions) — exact matches on every node count. See `BUILD_NOTES.md` in the build history for the full test record.
