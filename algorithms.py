
from typing import Callable, Dict, Optional, Tuple, List
from collections import deque
from itertools import count
import heapq
import time

from grid import Grid, Node

SearchResult = Tuple[Dict[Node, Optional[Node]], Dict[Node, float], float, int]

ProgressCb = Callable[[Node, str], Optional[bool]]

def _notify(cb: Optional[ProgressCb], node: Node, event: str) -> bool:
    if cb is None:
        return False
    return bool(cb(node, event))

def reconstruct_path(came_from: Dict[Node, Optional[Node]], start: Node, goal: Node) -> List[Node]:
    path = []
    cur = goal
    while cur is not None and cur in came_from:
        path.append(cur)
        if cur == start: break
        cur = came_from[cur]
    path.reverse()
    return path

def bfs(grid: Grid, start: Node, goal: Node,
        progress_cb: Optional[ProgressCb] = None) -> SearchResult:
    t0 = time.perf_counter()
    frontier = deque([start])
    came_from: Dict[Node, Optional[Node]] = {start: None}
    cost_so_far: Dict[Node, float] = {start: 0}
    nodes_expanded = 0

    _notify(progress_cb, start, "discover")

    while frontier:
        current = frontier.popleft()
        nodes_expanded += 1
        if _notify(progress_cb, current, "expand"):
            break
        if current == goal:
            _notify(progress_cb, current, "found")
            break
        for nxt in grid.neighbors(current):
            if nxt not in came_from:
                came_from[nxt] = current
                cost_so_far[nxt] = cost_so_far[current] + 1
                frontier.append(nxt)
                _notify(progress_cb, nxt, "discover")

    elapsed = time.perf_counter() - t0
    return came_from, cost_so_far, elapsed, nodes_expanded

def dijkstra(grid: Grid, start: Node, goal: Node, progress_cb: Optional[ProgressCb] = None) -> SearchResult:
    t0 = time.perf_counter()
    counter = count()
    pq: List[Tuple[float, int, Node]] = [(0, next(counter), start)]
    came_from: Dict[Node, Optional[Node]] = {start: None}
    cost_so_far: Dict[Node, float] = {start: 0}
    nodes_expanded = 0

    _notify(progress_cb, start, "discover")

    while pq:
        cur_cost, _, current = heapq.heappop(pq)
        if cur_cost > cost_so_far[current]:
            continue
        nodes_expanded += 1
        if _notify(progress_cb, current, "expand"):
            break
        if current == goal:
            _notify(progress_cb, current, "found")
            break
        for nxt in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(nxt)
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                came_from[nxt] = current
                heapq.heappush(pq, (new_cost, next(counter), nxt))
                _notify(progress_cb, nxt, "discover")

    elapsed = time.perf_counter() - t0
    return came_from, cost_so_far, elapsed, nodes_expanded

def astar(grid: Grid, start: Node, goal: Node, heuristic: Callable[[Node, Node], float],
            progress_cb: Optional[ProgressCb] = None) -> SearchResult:
    t0 = time.perf_counter()
    counter = count()
    pq: List[Tuple[float, int, Node]] = [(0, next(counter), start)]
    came_from: Dict[Node, Optional[Node]] = {start: None}
    g: Dict[Node, float] = {start: 0}
    nodes_expanded = 0

    _notify(progress_cb, start, "discover")

    while pq:
        f_score, _, current = heapq.heappop(pq)
        if f_score > g[current] + heuristic(current, goal):
            continue
        nodes_expanded += 1
        if _notify(progress_cb, current, "expand"):
            break
        if current == goal:
            _notify(progress_cb, current, "found")
            break
        for nxt in grid.neighbors(current):
            new_g = g[current] + grid.cost(nxt)
            if nxt not in g or new_g < g[nxt]:
                g[nxt] = new_g
                came_from[nxt] = current
                f = new_g + heuristic(nxt, goal)
                heapq.heappush(pq, (f, next(counter), nxt))
                _notify(progress_cb, nxt, "discover")

    elapsed = time.perf_counter() - t0
    return came_from, g, elapsed, nodes_expanded
