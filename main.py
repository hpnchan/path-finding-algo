
import pygame as pg
from grid import Grid, Node
from visual import Visual
from algorithms import bfs, dijkstra, astar, reconstruct_path
from heuristics import manhattan, octile
from constants import *

def run():
    grid = Grid(GRID_ROWS, GRID_COLS, diagonal=False)
    vis = Visual(grid)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_q):
                    running = False
                elif event.key == pg.K_d:
                    grid.diagonal = not grid.diagonal
                    vis.metrics["diag"] = grid.diagonal
                elif event.key == pg.K_c:
                    vis.clear_search_layers()
                elif event.key == pg.K_r:
                    grid.reset_map()
                    vis.start = None
                    vis.goal = None
                    vis.clear_search_layers()
                elif event.key == pg.K_w:
                    vis.paint_weight = not vis.paint_weight
                elif event.key == pg.K_g:
                    vis.random_obstacles(0.10)
                elif event.key in (pg.K_1, pg.K_2, pg.K_3):
                    if vis.start and vis.goal:
                        vis.clear_search_layers()
                        algo_key = {pg.K_1:"BFS", pg.K_2:"Dijkstra", pg.K_3:"A*"}[event.key]
                        heuristic = manhattan if not grid.diagonal else octile

                        def progress_cb(n: Node, phase: str) -> bool:
                            nonlocal running
                            if phase == "discover":
                                if n != vis.start and n != vis.goal:
                                    vis.frontier.add(n)
                            else:
                                vis.frontier.discard(n)
                                if n != vis.start and n != vis.goal:
                                    vis.visited.add(n)
                            vis.draw(throttle=False)
                            for pending in pg.event.get():
                                if pending.type == pg.QUIT:
                                    running = False
                                    return True
                                if pending.type == pg.KEYDOWN and pending.key in (pg.K_ESCAPE, pg.K_q):
                                    running = False
                                    return True
                            return False

                        if algo_key == "BFS":
                            came, cost, t, expanded = bfs(grid, vis.start, vis.goal, progress_cb=progress_cb)
                        elif algo_key == "Dijkstra":
                            came, cost, t, expanded = dijkstra(grid, vis.start, vis.goal, progress_cb=progress_cb)
                        else:
                            came, cost, t, expanded = astar(grid, vis.start, vis.goal, heuristic=heuristic, progress_cb=progress_cb)

                        path = reconstruct_path(came, vis.start, vis.goal)
                        vis.set_path(path)
                        vis.frontier.clear()
                        total_cost = cost.get(vis.goal, float('inf'))
                        vis.set_metrics(algo_key, expanded, t, total_cost, len(path))
                elif event.key == pg.K_s:
                    vis.set_start(pg.mouse.get_pos())
                elif event.key == pg.K_e:
                    vis.set_goal(pg.mouse.get_pos())

        buttons = pg.mouse.get_pressed(3)
        if any(buttons):
            vis.handle_mouse(buttons, pg.mouse.get_pos())

        vis.draw()

    pg.quit()

if __name__ == "__main__":
    run()
