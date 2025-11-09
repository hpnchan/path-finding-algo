
import pygame as pg
from typing import Optional, Tuple, List
from grid import Grid, Node
from constants import *

class Visual:
    def __init__(self, grid: Grid):
        pg.init()
        w = GRID_COLS * (CELL_SIZE + MARGIN) + MARGIN
        h = GRID_ROWS * (CELL_SIZE + MARGIN) + 120
        self.screen = pg.display.set_mode((w, h))
        pg.display.set_caption(WINDOW_TITLE)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("consolas", 18)
        self.grid = grid
        self.frontier: set[Node] = set()
        self.visited: set[Node] = set()
        self.path: List[Node] = []
        self.start: Optional[Node] = None
        self.goal: Optional[Node] = None
        self.paint_weight = False

        self.metrics = {
            "algo": "",
            "expanded": 0,
            "time": 0.0,
            "cost": 0.0,
            "len": 0,
            "diag": self.grid.diagonal,
        }

    def to_cell(self, pos) -> tuple[int,int]:
        x, y = pos
        c = (x - MARGIN) // (CELL_SIZE + MARGIN)
        r = (y - MARGIN) // (CELL_SIZE + MARGIN)
        if 0 <= r < self.grid.rows and 0 <= c < self.grid.cols:
            return (r, c)
        return (-1, -1)

    def draw(self, throttle: bool = True):
        self.screen.fill(COL_BG)
        # grid
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                x = MARGIN + c*(CELL_SIZE+MARGIN)
                y = MARGIN + r*(CELL_SIZE+MARGIN)
                rect = pg.Rect(x, y, CELL_SIZE, CELL_SIZE)
                cell = self.grid.cells[(r,c)]
                col = COL_EMPTY
                if cell.wall:
                    col = COL_WALL
                elif cell.weight > 1:
                    col = COL_WEIGHT

                pg.draw.rect(self.screen, col, rect, border_radius=4)

                node = Node(r,c)
                if node in self.visited:
                    pg.draw.rect(self.screen, COL_VISITED, rect, border_radius=4)
                if node in self.frontier:
                    pg.draw.rect(self.screen, COL_FRONTIER, rect, border_radius=4)
                if node in self.path:
                    pg.draw.rect(self.screen, COL_PATH, rect, border_radius=4)

        # start & goal
        if self.start:
            rs, cs = self.start.r, self.start.c
            x = MARGIN + cs*(CELL_SIZE+MARGIN)
            y = MARGIN + rs*(CELL_SIZE+MARGIN)
            pg.draw.rect(self.screen, COL_START, (x,y,CELL_SIZE,CELL_SIZE), border_radius=4)
        if self.goal:
            rg, cg = self.goal.r, self.goal.c
            x = MARGIN + cg*(CELL_SIZE+MARGIN)
            y = MARGIN + rg*(CELL_SIZE+MARGIN)
            pg.draw.rect(self.screen, COL_GOAL, (x,y,CELL_SIZE,CELL_SIZE), border_radius=4)

        # panel
        panel_y = MARGIN + self.grid.rows*(CELL_SIZE+MARGIN) + 10
        lines = [
            f"[1] BFS   [2] Dijkstra   [3] A*   [D] Diagonal={self.grid.diagonal}",
            f"[S] Start  [E] End  [W] WeightPaint={self.paint_weight}  [G] Random  [C] Clear  [R] Reset",
            f"Algo: {self.metrics['algo']} | Expanded: {self.metrics['expanded']} | Time: {self.metrics['time']*1000:.2f} ms | Cost: {self.metrics['cost']:.1f} | PathLen: {self.metrics['len']}",
        ]
        for i, line in enumerate(lines):
            surf = self.font.render(line, True, COL_TEXT)
            self.screen.blit(surf, (MARGIN, panel_y + i*22))

        pg.display.flip()
        if throttle:
            self.clock.tick(FPS)

    def set_path(self, path):
        self.path = path

    def set_metrics(self, algo, expanded, t, cost, length):
        self.metrics.update({"algo": algo, "expanded": expanded, "time": t, "cost": cost, "len": length})

    def clear_search_layers(self):
        self.frontier.clear()
        self.visited.clear()
        self.path = []

    def random_obstacles(self, p=0.10):
        import random
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                if random.random() < p:
                    self.grid.cells[(r,c)].wall = True

    def handle_mouse(self, buttons, pos):
        r, c = self.to_cell(pos)
        if r == -1: return
        node = Node(r,c)
        if buttons[0]:  # left: add wall / weight
            if self.paint_weight:
                self.grid.cells[(r,c)].weight = 5
                self.grid.cells[(r,c)].wall = False
            else:
                if node != self.start and node != self.goal:
                    self.grid.cells[(r,c)].wall = True
        if buttons[2]:  # right: remove (wall/weight)
            self.grid.cells[(r,c)].wall = False
            self.grid.cells[(r,c)].weight = 1

    def set_start(self, pos):
        r, c = self.to_cell(pos)
        if r == -1: return
        n = Node(r,c)
        if not self.grid.cells[(r,c)].wall:
            self.start = n

    def set_goal(self, pos):
        r, c = self.to_cell(pos)
        if r == -1: return
        n = Node(r,c)
        if not self.grid.cells[(r,c)].wall:
            self.goal = n
