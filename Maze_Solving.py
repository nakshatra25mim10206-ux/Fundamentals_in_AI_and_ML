import heapq
import random
import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterator, List, Optional, Set, Tuple
import pygame
Cell = Tuple[int, int]
SolverStep = Tuple[Set[Cell], Set[Cell], Optional[List[Cell]]]
SolverFn = Callable[[List[List[int]], Cell, Cell], Iterator[SolverStep]]

ROWS, COLS = 21, 21
CELL_SIZE = 28
HEADER_HEIGHT = 60
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + HEADER_HEIGHT
FPS = 60
STEPS_PER_FRAME = 1
MAZE_RECURSION_LIMIT = 5000


class Palette:
    BLACK    = (10,  10,  20)
    WHITE    = (220, 220, 230)
    WALL     = (30,  30,  50)
    OPEN     = (60,  60,  90)
    VISITED  = (50, 100, 180)
    FRONTIER = (80, 180, 255)
    PATH     = (80, 255, 160)
    START    = (255, 210, 80)
    END      = (255,  80,  80)
    HINT     = (100, 100, 130)

def generate_maze(rows: int, cols: int) -> List[List[int]]:
    grid = [[0] * cols for _ in range(rows)]

    def carve(r: int, c: int) -> None:
        grid[r][c] = 1
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                grid[r + dr // 2][c + dc // 2] = 1  # knock down the wall between
                carve(nr, nc)

    sys.setrecursionlimit(MAZE_RECURSION_LIMIT)
    carve(1, 1)
    return grid


def neighbors(grid: List[List[int]], r: int, c: int) -> Iterator[Cell]:
    rows, cols = len(grid), len(grid[0])
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
            yield (nr, nc)


def reconstruct_path(came_from: Dict[Cell, Cell], node: Cell) -> List[Cell]:
    trail = [node]
    while node in came_from:
        node = came_from[node]
        trail.append(node)
    return trail

def astar(grid: List[List[int]], start: Cell, end: Cell) -> Iterator[SolverStep]:
    def heuristic(n: Cell) -> int:
        return abs(n[0] - end[0]) + abs(n[1] - end[1])

    open_heap = [(heuristic(start), 0, start)]
    came_from: Dict[Cell, Cell] = {}
    best_cost = {start: 0}
    visited: Set[Cell] = set()
    frontier = {start}

    while open_heap:
        _, cost, current = heapq.heappop(open_heap)
        frontier.discard(current)

        if current == end:
            yield visited, frontier, reconstruct_path(came_from, current)
            return

        visited.add(current)
        for neighbor in neighbors(grid, *current):
            new_cost = cost + 1
            if new_cost < best_cost.get(neighbor, float("inf")):
                came_from[neighbor] = current
                best_cost[neighbor] = new_cost
                heapq.heappush(open_heap, (new_cost + heuristic(neighbor), new_cost, neighbor))
                frontier.add(neighbor)

        yield visited, frontier, None

    yield visited, set(), None


def bfs(grid: List[List[int]], start: Cell, end: Cell) -> Iterator[SolverStep]:
    queue = deque([start])
    came_from: Dict[Cell, Cell] = {}
    discovered = {start}
    visited: Set[Cell] = set()
    frontier = {start}

    while queue:
        current = queue.popleft()
        frontier.discard(current)

        if current == end:
            yield visited, frontier, reconstruct_path(came_from, current)
            return

        visited.add(current)
        for neighbor in neighbors(grid, *current):
            if neighbor not in discovered:
                came_from[neighbor] = current
                discovered.add(neighbor)
                frontier.add(neighbor)
                queue.append(neighbor)

        yield visited, frontier, None

    yield visited, set(), None


def dfs(grid: List[List[int]], start: Cell, end: Cell) -> Iterator[SolverStep]:
    stack = [start]
    came_from: Dict[Cell, Cell] = {}
    visited: Set[Cell] = set()
    frontier = {start}

    while stack:
        current = stack.pop()
        frontier.discard(current)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            yield visited, frontier, reconstruct_path(came_from, current)
            return

        for neighbor in neighbors(grid, *current):
            if neighbor not in visited:
                came_from[neighbor] = current
                frontier.add(neighbor)
                stack.append(neighbor)

        yield visited, frontier, None

    yield visited, set(), None


SOLVERS: Dict[int, Tuple[str, SolverFn]] = {
    pygame.K_1: ("A*", astar),
    pygame.K_2: ("BFS", bfs),
    pygame.K_3: ("DFS", dfs),
}

def cell_color(
    pos: Cell,
    grid: List[List[int]],
    start: Cell,
    end: Cell,
    path_set: Set[Cell],
    frontier: Set[Cell],
    visited: Set[Cell],
) -> Tuple[int, int, int]:
    if pos == start:
        return Palette.START
    if pos == end:
        return Palette.END
    if pos in path_set:
        return Palette.PATH
    if pos in frontier:
        return Palette.FRONTIER
    if pos in visited:
        return Palette.VISITED
    r, c = pos
    return Palette.WALL if grid[r][c] == 0 else Palette.OPEN


def draw(
    screen: pygame.Surface,
    font: "pygame.font.Font",
    grid: List[List[int]],
    visited: Set[Cell],
    frontier: Set[Cell],
    path: List[Cell],
    start: Cell,
    end: Cell,
    label: str,
) -> None:
    screen.fill(Palette.BLACK)
    path_set = set(path) if path else set()

    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE + HEADER_HEIGHT, CELL_SIZE, CELL_SIZE)
            color = cell_color((r, c), grid, start, end, path_set, frontier, visited)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, Palette.BLACK, rect, 1)

    info = font.render(label, True, Palette.WHITE)
    hint = font.render("1:A*  2:BFS  3:DFS  R:New  SPACE:Pause  ESC:Quit", True, Palette.HINT)
    screen.blit(info, (10, 10))
    screen.blit(hint, (10, 35))

@dataclass
class SolverState:
    generator: Optional[Iterator[SolverStep]] = None
    visited: Set[Cell] = field(default_factory=set)
    frontier: Set[Cell] = field(default_factory=set)
    path: List[Cell] = field(default_factory=list)
    paused: bool = False

    def start(
        self, name: str, solver: SolverFn,
        grid: List[List[int]], start_cell: Cell, end_cell: Cell,
    ) -> str:
        self.generator = solver(grid, start_cell, end_cell)
        self.visited, self.frontier, self.path = set(), set(), []
        self.paused = False
        return f"Running {name} ..."

    def reset(self) -> None:
        self.generator, self.visited, self.frontier, self.path = None, set(), set(), []

    def advance(self, steps: int) -> Optional[str]:
        if not self.generator or self.paused:
            return None

        for _ in range(steps):
            try:
                self.visited, self.frontier, result = next(self.generator)
            except StopIteration:
                self.generator = None
                return None if self.path else "No path found."
            if result:
                self.path = result
                self.generator = None
                return f"Done! Path length: {len(self.path)}  |  Visited: {len(self.visited)}"
        return None


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Solver")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 18, bold=True)

        self.grid = generate_maze(ROWS, COLS)
        self.start_cell: Cell = (1, 1)
        self.end_cell: Cell = (ROWS - 2, COLS - 2)

        self.solver = SolverState()
        self.label = "Press 1, 2, or 3 to solve  |  R for new maze"
        self.running = True

    def new_maze(self) -> None:
        self.grid = generate_maze(ROWS, COLS)
        self.solver.reset()
        self.label = "New maze! Press 1, 2, or 3 to solve."

    def handle_keydown(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_r:
            self.new_maze()
        elif key == pygame.K_SPACE:
            self.solver.paused = not self.solver.paused
        elif key in SOLVERS:
            name, solver_fn = SOLVERS[key]
            self.label = self.solver.start(name, solver_fn, self.grid, self.start_cell, self.end_cell)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def update(self) -> None:
        new_label = self.solver.advance(STEPS_PER_FRAME)
        if new_label is not None:
            self.label = new_label

    def render(self) -> None:
        draw(
            self.screen, self.font, self.grid,
            self.solver.visited, self.solver.frontier, self.solver.path,
            self.start_cell, self.end_cell, self.label,
        )
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()