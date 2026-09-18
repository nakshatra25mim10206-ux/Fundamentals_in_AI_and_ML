

import pygame
import random
import heapq
import sys
from collections import deque

ROWS, COLS  = 21, 21          
CELL        = 28              
WIDTH       = COLS * CELL
HEIGHT      = ROWS * CELL + 60  
FPS         = 60
STEPS_FRAME = 1                 

BLACK    = (10,  10,  20)
WHITE    = (220, 220, 230)
WALL     = (30,  30,  50)
OPEN     = (60,  60,  90)
VISITED  = (50, 100, 180)
FRONTIER = (80, 180, 255)
PATH     = (80, 255, 160)
START    = (255, 210, 80)
END      = (255,  80,  80)

def maze(rows, cols):
    grid = [[0] * cols for _ in range(rows)]  

    def carve(r, c):
        grid[r][c] = 1
        dirs = [(0,2),(0,-2),(2,0),(-2,0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                grid[r+dr//2][c+dc//2] = 1
                carve(nr, nc)

    sys.setrecursionlimit(5000)
    carve(1, 1)
    return grid

def available_moves(grid, r, c):
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 1:
            yield (nr, nc)

def path(prior, node):
    path = []
    while node in prior:
        path.append(node)
        node = prior[node]
    path.append(node)
    return path

def astar(grid, start, end):
    def h(n): return abs(n[0]-end[0]) + abs(n[1]-end[1])
    heap = [(h(start), 0, start)]
    prior = {}
    g = {start: 0}
    seen, gonna_see = set(), {start}

    while heap:
        _, cost, cur = heapq.heappop(heap)
        gonna_see.discard(cur)
        if cur == end:
            yield seen, gonna_see, path(prior, cur)
            return
        seen.add(cur)
        for nb in available_moves(grid, *cur):
            new_g = cost + 1
            if new_g < g.get(nb, float('inf')):
                prior[nb] = cur
                g[nb] = new_g
                heapq.heappush(heap, (new_g + h(nb), new_g, nb))
                gonna_see.add(nb)
        yield seen, gonna_see, None

    yield seen, set(), None

def bfs(grid, start, end):
    queue = deque([start])
    prior = {start: None}
    seen, gonna_see = set(), {start}

    while queue:
        cur = queue.popleft()
        gonna_see.discard(cur)
        if cur == end:
            yield seen, gonna_see, path(prior, cur)
            return
        seen.add(cur)
        for nb in available_moves(grid, *cur):
            if nb not in prior:
                prior[nb] = cur
                gonna_see.add(nb)
                queue.append(nb)
        yield seen, gonna_see, None

    yield seen, set(), None

def dfs(grid, start, end):
    stack = [start]
    prior = {start: None}
    seen, gonna_see = set(), {start}

    while stack:
        cur = stack.pop()
        gonna_see.discard(cur)
        if cur in seen:
            continue
        seen.add(cur)
        if cur == end:
            yield seen, gonna_see, path(prior, cur)
            return
        for nb in available_moves(grid, *cur):
            if nb not in seen:
                prior[nb] = cur
                gonna_see.add(nb)
                stack.append(nb)
        yield seen, gonna_see, None

    yield seen, set(), None

def draw(screen, grid, seen, gonna_see, path, start, end, label):
    screen.fill(BLACK)
    path_set = set(path) if path else set()

    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL, r*CELL+60, CELL, CELL)
            pos  = (r, c)
            if pos == start:            col = START
            elif pos == end:            col = END
            elif pos in path_set:       col = PATH
            elif pos in gonna_see:       col = FRONTIER
            elif pos in seen:        col = VISITED
            elif grid[r][c] == 0:       col = WALL
            else:                       col = OPEN
            pygame.draw.rect(screen, col, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    font = pygame.font.SysFont("monospace", 18, bold=True)
    info = font.render(label, True, WHITE)
    hint = font.render("1:A*  2:BFS  3:DFS  R:New  SPACE:Pause  ESC:Quit", True, (100,100,130))
    screen.blit(info, (10, 10))
    screen.blit(hint, (10, 35))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Solver")
    clock  = pygame.time.Clock()

    grid  = maze(ROWS, COLS)
    start = (1, 1)
    end   = (ROWS-2, COLS-2)

    gen      = None
    seen  = set()
    gonna_see = set()
    path     = []
    paused   = False
    label    = "Press 1, 2, or 3 to solve  |  R for new maze"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
               event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = maze(ROWS, COLS)
                    gen, seen, gonna_see, path = None, set(), set(), []
                    label = "New maze! Press 1, 2, or 3 to solve."

                elif event.key == pygame.K_1:
                    gen, seen, gonna_see, path = astar(grid, start, end), set(), set(), []
                    label = "Running A* ..."
                    paused = False

                elif event.key == pygame.K_2:
                    gen, seen, gonna_see, path = bfs(grid, start, end), set(), set(), []
                    label = "Running BFS ..."
                    paused = False

                elif event.key == pygame.K_3:
                    gen, seen, gonna_see, path = dfs(grid, start, end), set(), set(), []
                    label = "Running DFS ..."
                    paused = False

                elif event.key == pygame.K_SPACE:
                    paused = not paused

        
        if gen and not paused:
            for _ in range(STEPS_FRAME):
                try:
                    seen, gonna_see, result = next(gen)
                    if result:
                        path  = result
                        label = f"Done! Path length: {len(path)}  |  Visited: {len(seen)}"
                        gen   = None
                        break
                except StopIteration:
                    gen   = None
                    label = "No path found." if not path else label
                    break

        draw(screen, grid, seen, gonna_see, path, start, end, label)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
