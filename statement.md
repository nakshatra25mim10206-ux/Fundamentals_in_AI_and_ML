# Project Statement

**Project:** Pathfinding Algorithm Visualizer
**Author:** [Your Full Name]

---

## Problem Statement

Pathfinding is a fundamental problem in computer science — used in GPS navigation, game AI, robotics, and network routing. Understanding *how* different search algorithms explore a search space, and *why* some guarantee an optimal path while others don't, is a core concept in Data Structures, Algorithms, and Artificial Intelligence education. However, this is typically taught through static pseudocode and diagrams, which make it difficult to build real intuition for how algorithms like A*, BFS, and DFS actually behave — which nodes they visit, in what order, and how efficiently they converge on a solution.

There is a need for an interactive, visual tool that lets a learner *see* these differences directly, rather than infer them from text alone.

---

## Scope

**In scope:**
- Procedural generation of a random, always-solvable maze on every run.
- Implementation of three pathfinding algorithms — A* Search, Breadth-First Search, and Depth-First Search — that can each be run on the identical maze layout for fair comparison.
- Real-time, step-by-step animated visualization of each algorithm's exploration (frontier, visited nodes, final path).
- Live on-screen statistics: number of nodes visited and length of the path found.
- Simple keyboard-driven controls for generating a new maze, selecting an algorithm, pausing/resuming, and quitting.
- Configurable maze size and animation speed via command-line arguments.

**Out of scope:**
- Persistent storage of past runs, results, or user data (the tool is a single-session, in-memory visualizer).
- Weighted terrain or non-uniform movement costs (all moves currently cost 1; Dijkstra's algorithm and weighted heuristics are noted as a future enhancement).
- A graphical menu system, mouse-based interaction, or web-based deployment — the interface is a single Pygame window driven entirely by the keyboard.
- Multiplayer or networked functionality of any kind.

---

## Target Users

- **Computer Science / AI students** learning graph traversal and heuristic search algorithms, who want to build intuition beyond pseudocode.
- **Educators and teaching assistants** looking for a lightweight, dependency-light demo to use in lectures or lab sessions on search algorithms.
- **Self-learners** preparing for coding interviews or coursework involving BFS, DFS, or A*, who want to visually verify their understanding of how each algorithm behaves.

---

## High-Level Features

- 🌀 Randomized maze generation using the Recursive Backtracker algorithm, guaranteeing a solvable maze with exactly one unique path between any two cells.
- 🧠 Three interchangeable, generator-based pathfinding algorithms: A* (Manhattan-distance heuristic), BFS, and DFS.
- 🎬 Real-time, frame-by-frame animation of the search process — not an instant "flash" result.
- 🎨 Consistent colour-coding across all three algorithms (start, end, wall, open, frontier, visited, final path) for intuitive visual comparison.
- 📊 Live statistics on nodes visited and path length, so efficiency differences can be measured, not just observed.
- ⌨️ Minimal, fully keyboard-driven interaction with on-screen control hints — no external documentation needed while using the tool.
- ⚙️ Adjustable maze size and animation speed via command-line flags, without editing source code.
