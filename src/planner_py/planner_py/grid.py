"""
Occupancy grid used by the planners.

Coordinate conventions (the same as robot_sim/scripts/grid_map.py):

* A cell is ``(ix, iy)``. ``ix`` grows in +x (right), ``iy`` grows in +y (up).
* The row-major index of a cell is ``iy * width + ix``.
* The lower-left corner of cell ``(0, 0)`` is the map origin ``(origin_x, origin_y)``.
* ``cell_to_world`` returns the *center* of a cell, in metres, in the ``map`` frame.

The planners work in cell units. A straight step costs 1.0 and a diagonal step costs
sqrt(2), so a path cost does not depend on the map resolution.
"""
from dataclasses import dataclass, field
import math
from typing import Iterator, List, Tuple

from nav_msgs.msg import OccupancyGrid

Cell = Tuple[int, int]

SQRT2 = math.sqrt(2.0)
# (dx, dy, step cost): the 4 straight neighbours first, then the 4 diagonal ones.
NEIGHBOR_OFFSETS = (
    (1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
    (1, 1, SQRT2), (1, -1, SQRT2), (-1, 1, SQRT2), (-1, -1, SQRT2),
)


@dataclass
class PlanResult:
    """What a planner returns when it finds a path."""

    path: List[Cell]
    """Cells from the start to the goal, both included."""

    cost: float
    """Length of the path in cell units (straight step 1.0, diagonal step sqrt(2))."""

    expanded: int
    """How many cells were taken out of the open set and expanded (for comparing planners)."""

    visited: List[Cell] = field(default_factory=list)
    """Optional: the expanded cells in order. When given, RViz shows them on /planner/visited."""


class Grid:
    """A grid in which every cell is either free or blocked."""

    def __init__(self, width, height, resolution, origin_x, origin_y, blocked):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.blocked = blocked  # bytearray, 1 = blocked, indexed by iy * width + ix

    @classmethod
    def from_occupancy_grid(cls, msg, robot_radius, unknown_is_blocked=True):
        """
        Build a grid from a nav_msgs/OccupancyGrid.

        Obstacle cells are inflated by ``robot_radius`` [m], so that a planner may treat the
        robot as a single point. Unknown cells (-1) are blocked when ``unknown_is_blocked``.
        """
        info = msg.info
        width, height, res = info.width, info.height, info.resolution
        blocked = bytearray(width * height)
        obstacles = []
        for i, v in enumerate(msg.data):
            if v >= 50:
                blocked[i] = 1
                obstacles.append(i)
            elif v < 0 and unknown_is_blocked:
                blocked[i] = 1

        radius = robot_radius / res
        reach = math.ceil(radius)
        disk = [(dx, dy) for dx in range(-reach, reach + 1) for dy in range(-reach, reach + 1)
                if dx * dx + dy * dy <= radius * radius]
        for i in obstacles:
            iy, ix = divmod(i, width)
            for dx, dy in disk:
                jx, jy = ix + dx, iy + dy
                if 0 <= jx < width and 0 <= jy < height:
                    blocked[jy * width + jx] = 1
        return cls(width, height, res, info.origin.position.x, info.origin.position.y, blocked)

    def in_bounds(self, ix, iy):
        return 0 <= ix < self.width and 0 <= iy < self.height

    def is_free(self, ix, iy):
        """Return True if the cell is inside the map and not blocked."""
        return self.in_bounds(ix, iy) and not self.blocked[iy * self.width + ix]

    def world_to_cell(self, x, y):
        """Return the cell that contains the world point (x, y) [m]. It may be out of bounds."""
        return (math.floor((x - self.origin_x) / self.resolution),
                math.floor((y - self.origin_y) / self.resolution))

    def cell_to_world(self, ix, iy):
        """Return the world coordinates (x, y) [m] of the center of a cell."""
        return (self.origin_x + (ix + 0.5) * self.resolution,
                self.origin_y + (iy + 0.5) * self.resolution)

    def neighbors(self, ix, iy) -> Iterator[Tuple[int, int, float]]:
        """
        Yield ``(jx, jy, step_cost)`` for every free 8-neighbour of a cell.

        A diagonal step is skipped when either of the two cells it passes between is blocked
        (no cutting corners). You may use this helper or write your own, for example with only
        4 neighbours, to see how the paths change.
        """
        for dx, dy, cost in NEIGHBOR_OFFSETS:
            jx, jy = ix + dx, iy + dy
            if not self.is_free(jx, jy):
                continue
            if dx != 0 and dy != 0:
                if not (self.is_free(ix + dx, iy) and self.is_free(ix, iy + dy)):
                    continue
            yield jx, jy, cost


def make_grid_msg(grid: Grid, data, frame_id, stamp) -> OccupancyGrid:
    """Wrap per-cell values (row-major, 0..100) in a nav_msgs/OccupancyGrid for RViz."""
    msg = OccupancyGrid()
    msg.header.frame_id = frame_id
    msg.header.stamp = stamp
    msg.info.resolution = grid.resolution
    msg.info.width = grid.width
    msg.info.height = grid.height
    msg.info.origin.position.x = grid.origin_x
    msg.info.origin.position.y = grid.origin_y
    msg.info.origin.orientation.w = 1.0
    msg.data = data
    return msg
