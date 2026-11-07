"""
Tests for the grid planners.

A test is skipped while the planner it needs still raises NotImplementedError, so the
suite stays green until you implement dijkstra() and astar(), then starts checking them.

    cd ~/ros2_ws/src/planner_py && python3 -m pytest test/test_algorithms.py -v
"""
import random

from planner_py.astar import astar
from planner_py.dijkstra import dijkstra
from planner_py.grid import Grid, SQRT2
import pytest

PLANNERS = [dijkstra, astar]


def parse(rows):
    """
    Build ``(grid, start, goal)`` from ASCII art.

    The first row is the TOP of the map (the largest iy). '#' is blocked, 'S' the start,
    'G' the goal, anything else is free.
    """
    height, width = len(rows), len(rows[0])
    blocked = bytearray(width * height)
    start = goal = None
    for r, line in enumerate(rows):
        iy = height - 1 - r
        for ix, ch in enumerate(line):
            if ch == '#':
                blocked[iy * width + ix] = 1
            elif ch == 'S':
                start = (ix, iy)
            elif ch == 'G':
                goal = (ix, iy)
    return Grid(width, height, 1.0, 0.0, 0.0, blocked), start, goal


def run(planner, grid, start, goal):
    try:
        return planner(grid, start, goal)
    except NotImplementedError:
        pytest.skip(f'{planner.__name__}() is not implemented yet')


def check_valid(grid, result, start, goal):
    """Assert that a result is a legal path and that its cost matches its steps."""
    path = result.path
    assert path[0] == start and path[-1] == goal
    cost = 0.0
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        dx, dy = bx - ax, by - ay
        assert max(abs(dx), abs(dy)) == 1, f'cells {(ax, ay)} and {(bx, by)} are not neighbours'
        if dx != 0 and dy != 0:
            assert grid.is_free(ax + dx, ay) and grid.is_free(ax, ay + dy), \
                f'the step {(ax, ay)} -> {(bx, by)} cuts a corner'
            cost += SQRT2
        else:
            cost += 1.0
    assert all(grid.is_free(*c) for c in path), 'the path goes through a blocked cell'
    assert result.cost == pytest.approx(cost), 'cost does not match the sum of the steps'


def random_case(rng, size=12, density=0.25):
    blocked = bytearray(1 if rng.random() < density else 0 for _ in range(size * size))
    grid = Grid(size, size, 1.0, 0.0, 0.0, blocked)
    free = [(i % size, i // size) for i in range(size * size) if not blocked[i]]
    if len(free) < 2:
        return None
    start, goal = rng.sample(free, 2)
    return grid, start, goal


@pytest.mark.parametrize('planner', PLANNERS)
def test_straight_line(planner):
    grid, start, goal = parse(['S...G'])
    result = run(planner, grid, start, goal)
    assert result.cost == pytest.approx(4.0)
    check_valid(grid, result, start, goal)


@pytest.mark.parametrize('planner', PLANNERS)
def test_diagonal(planner):
    grid, start, goal = parse(['...G', '....', '....', 'S...'])
    result = run(planner, grid, start, goal)
    assert result.cost == pytest.approx(3 * SQRT2)
    check_valid(grid, result, start, goal)


@pytest.mark.parametrize('planner', PLANNERS)
def test_detour_around_wall(planner):
    # The only way through the wall is the bottom cell (2, 0). Going from (2, 0) up to the
    # right is not allowed diagonally (it would cut the corner of the wall), so the best path
    # is 3 straight steps along the bottom, then 1 diagonal and 2 straight steps up.
    grid, start, goal = parse(['..#.G',
                               '..#..',
                               '..#..',
                               'S....'])
    result = run(planner, grid, start, goal)
    assert result.cost == pytest.approx(5 + SQRT2)
    check_valid(grid, result, start, goal)


@pytest.mark.parametrize('planner', PLANNERS)
def test_no_path_returns_none(planner):
    grid, start, goal = parse(['S.#.G',
                               '..#..',
                               '..#..'])
    assert run(planner, grid, start, goal) is None


@pytest.mark.parametrize('planner', PLANNERS)
def test_start_equals_goal(planner):
    grid, start, _ = parse(['S...'])
    result = run(planner, grid, start, start)
    assert result.path == [start]
    assert result.cost == pytest.approx(0.0)


@pytest.mark.parametrize('planner', PLANNERS)
def test_paths_are_valid_on_random_grids(planner):
    rng = random.Random(1234)
    found = 0
    for _ in range(40):
        case = random_case(rng)
        if case is None:
            continue
        grid, start, goal = case
        result = run(planner, grid, start, goal)
        if result is not None:
            check_valid(grid, result, start, goal)
            found += 1
    assert found > 0, 'the random grids should contain reachable goals'


def test_astar_cost_equals_dijkstra_cost():
    """A* with a consistent heuristic must find paths as short as Dijkstra's."""
    rng = random.Random(99)
    compared = 0
    for _ in range(60):
        case = random_case(rng)
        if case is None:
            continue
        grid, start, goal = case
        reference = run(dijkstra, grid, start, goal)
        result = run(astar, grid, start, goal)
        if reference is None:
            assert result is None, f'A* found a path from {start} to {goal}, Dijkstra did not'
        else:
            assert result is not None, f'A* found no path from {start} to {goal}'
            assert result.cost == pytest.approx(reference.cost), \
                f'A* cost {result.cost} != Dijkstra cost {reference.cost} for {start} -> {goal}'
            compared += 1
    assert compared > 0
