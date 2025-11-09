
from grid import Node
import math

def manhattan(a: Node, b: Node) -> float:
    return abs(a.r - b.r) + abs(a.c - b.c)

def euclidean(a: Node, b: Node) -> float:
    return ((a.r - b.r)**2 + (a.c - b.c)**2) ** 0.5

def octile(a: Node, b: Node) -> float:
    # For 8-direction moves: cost = max(dx,dy) + (sqrt(2) - 1)*min(dx,dy)
    dx = abs(a.r - b.r)
    dy = abs(a.c - b.c)
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
