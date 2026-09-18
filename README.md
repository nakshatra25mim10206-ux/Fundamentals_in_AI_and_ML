# 🧩 Pathfinding Algorithm Visualizer

A real-time visualizer that generates random mazes and solves them using three classic AI search algorithms — **A\***, **Breadth-First Search (BFS)**, and **Depth-First Search (DFS)**.

Built with Python and Pygame.

---

## UI Overview

<img width="736" height="852" alt="image" src="https://github.com/user-attachments/assets/44582990-1a62-4cc1-91f6-02b928f52039" />

---

## Overview

Pathfinding is a fundamental problem in computer science — used in GPS navigation, game AI, robotics, and network routing. Reading pseudocode makes it hard to *feel* how different algorithms explore a search space, and why some guarantee the shortest path while others don't.

This project makes that visible: a random maze is generated on every run, and the selected algorithm is animated step-by-step as it searches for a path from start to end — with the frontier, visited cells, and final path all color-coded in real time.

---

## Algorithms Implemented

| Algorithm | Strategy | Optimal Path? | Uses Heuristic? |
|---|---|---|---|
| **A\*** | Best-first (f = g + h) | ✅ Yes | ✅ Manhattan distance |
| **BFS** | Level-by-level expansion | ✅ Yes | ❌ No |
| **DFS** | Deepest node first | ❌ No | ❌ No |

---

## Features

- 🌀 Random maze generation using the **Recursive Backtracker** algorithm
- 🎬 Real-time, step-by-step animation of each algorithm
- 🎨 Color-coded visualization — frontier, visited nodes, and final path
- 📊 Live stats — nodes visited and path length
- ⚡ Compare algorithms on the same maze by pressing `1`, `2`, `3`
- ⚙️ Adjustable maze size and animation speed via CLI

---

## Tech Stack

- **Language:** Python 3.8+
- **Rendering & Input:** [Pygame](https://www.pygame.org/) (>= 2.5.0)
- **Data structures:** `heapq` (priority queue for A*), `collections.deque` (queue for BFS)

---

## Requirements

- Python 3.8+
- A display (monitor)

---

## Installation

```bash
git clone https://github.com/<your-username>/maze-solver.git
cd Maze_Solving
pip install -r requirements.txt
```

---

## Usage

```bash
# Default (21x21 maze, medium speed)
python Maze_Solving.py

# Custom maze size
python Maze_Solving.py --size 31

# Animation speed
python Maze_Solving.py --speed fast
python Maze_Solving.py --speed slow

# Combine
python Maze_Solving.py --size 25 --speed fast
```

### Controls

| Key | Action |
|---|---|
| `1` | Run A* Search |
| `2` | Run Breadth-First Search |
| `3` | Run Depth-First Search |
| `R` | Generate new random maze |
| `SPACE` | Pause / Resume |
| `ESC` | Quit |

---

## Testing

There's no automated test suite — the app is verified manually:

1. Launch the app and confirm a solvable maze is drawn.
2. Press `1`, `2`, and `3` on the same maze and confirm each algorithm completes and highlights a valid path from start to end.
3. Press `R` a few times to confirm a new, solvable maze is generated each time.
4. Press `SPACE` mid-run to confirm the animation pauses and resumes correctly.
5. Try `--size 11` and `--size 41` to confirm the app scales to smaller and larger grids.

Since `astar()`, `bfs()`, and `dfs()` are plain functions of `(grid, start, end)` with no Pygame dependency, they can also be imported directly in a Python shell to check path lengths and visited-node counts without launching the graphical window.

---

## Project Structure

```
maze-solver/
├── Maze_Solving.py   # Main application
├── requirements.txt  # Dependencies
├── statement.md      # Problem statement, scope, target users
└── README.md         # This file
```

---

## How It Works

1. **Maze Generation** — Recursive Backtracker (DFS-based) carves passages through a grid of walls, producing a perfect maze with exactly one path between any two points.
2. **Algorithm runs** — The selected algorithm explores the maze step by step, yielding its current state (visited nodes, frontier) at each step.
3. **Visualization** — Pygame renders each state in real time, color-coding visited nodes, the active frontier, and the final solution path.
4. **Comparison** — Running different algorithms on the same maze shows clearly why A* visits far fewer nodes than BFS, and why DFS finds a path quickly but not optimally.

---

## Future Improvements

- Split into separate modules (`maze_generator.py`, `algorithms/`, `renderer.py`)
- Add weighted terrain to demonstrate Dijkstra's algorithm
- Add automated unit tests (`pytest`)
- Support diagonal movement and alternative heuristics

---

## Author

Nakshatra Kundnani — https://github.com/nakshatra25mim10206-ux

## License

https://github.com/nakshatra25mim10206-ux/Fundamentals_in_AI_and_ML/blob/main/LICENSE
