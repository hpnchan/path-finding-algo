
from dataclasses import dataclass, field
from typing import Tuple, List, Dict

@dataclass(eq=True, frozen=True)
class Node:
    r: int
    c: int

@dataclass
class Cell:
    wall: bool = False
    weight: int = 1

@dataclass
class Grid:
    rows: int
    cols: int
    diagonal: bool = False
    cells: Dict[Tuple[int,int], Cell] = field(default_factory=dict)

    def __post_init__(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[(r,c)] = Cell()

    def in_bounds(self, n: Node) -> bool:
        return 0 <= n.r < self.rows and 0 <= n.c < self.cols

    def passable(self, n: Node) -> bool:
        return not self.cells[(n.r, n.c)].wall

    def cost(self, n: Node) -> int:
        return self.cells[(n.r, n.c)].weight

    def neighbors(self, n: Node) -> List[Node]:
        dirs4 = [(1,0),(-1,0),(0,1),(0,-1)]
        dirs8 = dirs4 + [(1,1),(1,-1),(-1,1),(-1,-1)]
        dirs = dirs8 if self.diagonal else dirs4
        res = [Node(n.r+dr, n.c+dc) for dr,dc in dirs]
        res = [p for p in res if self.in_bounds(p) and self.passable(p)]
        return res

    def clear_search(self):
        # no-op here, visual layer manages colors; kept for symmetry
        pass

    def reset_map(self):
        for k in self.cells:
            self.cells[k] = Cell()
