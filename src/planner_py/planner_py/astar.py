"""A* shortest path on a grid. Write your implementation in ``astar()``."""
from typing import Optional

from planner_py.grid import Cell, Grid, PlanResult


def astar(grid: Grid, start: Cell, goal: Cell) -> Optional[PlanResult]:
    """
    Find the shortest path from ``start`` to ``goal`` with a heuristic.

    Same contract as ``dijkstra()``. With an admissible, consistent heuristic the cost must be
    equal to the Dijkstra cost, and ``expanded`` should be smaller. The tests in
    ``test/test_algorithms.py`` check the equal cost.

    Costs are in cell units: a straight step is 1.0 and a diagonal step is sqrt(2), so think
    about which heuristic fits an 8-connected grid (Manhattan distance would overestimate).
    """
    raise NotImplementedError('TODO: implement astar()')
