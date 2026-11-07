"""Dijkstra's shortest path on a grid. Write your implementation in ``dijkstra()``."""
from typing import Optional

from planner_py.grid import Cell, Grid, PlanResult


def dijkstra(grid: Grid, start: Cell, goal: Cell) -> Optional[PlanResult]:
    """
    Find the shortest path from ``start`` to ``goal``.

    The node already checked that ``start`` and ``goal`` are free cells inside the map.
    Return a ``PlanResult``, or ``None`` when the goal cannot be reached.

    Useful pieces from ``planner_py.grid``:

    * ``grid.neighbors(ix, iy)`` yields ``(jx, jy, step_cost)`` of the free 8-neighbours.
    * ``grid.is_free(ix, iy)`` and ``grid.width`` / ``grid.height``.
    * ``PlanResult(path, cost, expanded, visited)``: ``visited`` is optional, but if you fill
      it with the expanded cells, RViz shows how far the search spread.
    """
    raise NotImplementedError('TODO: implement dijkstra()')
