import argparse
from collections import deque
import math
import pathlib
import sys

from grid_map import load_map

def obstacle_set(gm):
    return {(ix, iy) for iy in range(gm.height) for ix in range(gm.width)
            if gm.is_occupied(ix, iy)}

def nearest(gm, cells, x, y, tol):
    ix, iy = gm.world_to_cell(x, y)
    reach = math.ceil(tol / gm.resolution) + 1
    best = math.inf
    for jy in range(iy - reach, iy + reach + 1):
        for jx in range(ix - reach, ix + reach + 1):
            if (jx, jy) in cells:
                cx, cy = gm.cell_center(jx, jy)
                best = min(best, math.hypot(cx - x, cy - y))
    return best


def visible_surface(truth, spawn_xy):
    start = truth.world_to_cell(*spawn_xy)
    seen, queue, surface = {start}, deque([start]), set()
    while queue:
        ix, iy = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            jx, jy = ix + dx, iy + dy
            if not truth.in_bounds(jx, jy):
                continue
            if truth.is_occupied(jx, jy):
                surface.add((jx, jy))
            elif truth.data[jy * truth.width + jx] == 0 and (jx, jy) not in seen:
                seen.add((jx, jy))
                queue.append((jx, jy))
    return surface


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('slam_yaml', help='map saved with map_saver_cli')
    ap.add_argument('truth', help='name of the world map, maps/<name>.yaml')
    ap.add_argument('--spawn', nargs=3, type=float, required=True, metavar=('X', 'Y', 'YAW'))
    ap.add_argument('--tol', type=float, default=0.10, help='distance tolerance [m]')
    ap.add_argument('--min-precision', type=float, default=0.90)
    ap.add_argument('--min-recall', type=float, default=0.80)
    args = ap.parse_args()

    maps_dir = pathlib.Path(__file__).resolve().parent.parent / 'maps'
    truth = load_map(maps_dir / f'{args.truth}.yaml')
    slam = load_map(args.slam_yaml)
    sx0, sy0, yaw = args.spawn
    c, s = math.cos(yaw), math.sin(yaw)

    truth_cells = obstacle_set(truth)
    slam_cells = obstacle_set(slam)
    if not slam_cells:
        sys.exit('FAIL: the SLAM map has no obstacle cells')

    errors = []
    for ix, iy in slam_cells:
        x, y = slam.cell_center(ix, iy)
        errors.append(nearest(truth, truth_cells, sx0 + x * c - y * s, sy0 + x * s + y * c,
                              args.tol))
    errors.sort()
    precision = sum(e <= args.tol for e in errors) / len(errors)

    surface = visible_surface(truth, (sx0, sy0))
    found = 0
    for ix, iy in surface:
        wx, wy = truth.cell_center(ix, iy)
        dx, dy = wx - sx0, wy - sy0
        if nearest(slam, slam_cells, dx * c + dy * s, -dx * s + dy * c, args.tol) <= args.tol:
            found += 1
    recall = found / len(surface)

    known = sum(1 for v in slam.data if v != -1)
    area = known * slam.resolution ** 2
    print(f'SLAM map: {slam.width}x{slam.height} cells, known area {area:.1f} m2, '
          f'{len(slam_cells)} obstacle cells')
    print(f'truth:    {len(truth_cells)} obstacle cells, '
          f'{len(surface)} of them visible from the start')
    finite = [e for e in errors if e < math.inf]
    median = finite[len(finite) // 2] if finite else math.nan
    print(f'precision (tol {args.tol} m): {100 * precision:.1f}%   median error {median:.3f} m')
    print(f'recall    (tol {args.tol} m): {100 * recall:.1f}%')
    ok = precision >= args.min_precision and recall >= args.min_recall
    print('PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
