#!/usr/bin/env python3
"""외부에서 받은 SLAM 지도(YAML+PGM)를 시뮬레이션용으로 정리하고 Gazebo 월드를 만든다.

    python3 -I prepare_map.py third_party/nav2_tb3_sandbox/tb3_sandbox.yaml tb3_sandbox \\
        --seal-unknown --fill-holes 400

원본은 그대로 두고 maps/<이름>.{pgm,yaml} 과 worlds/<이름>.sdf 를 새로 만든다.

  --seal-unknown  빈 곳과 (8방향으로) 맞닿은 '모름' 셀을 장애물로 바꿔 벽의 틈을 막는다.
                  틈이 있으면 로봇이나 LiDAR 빔이 지도 밖으로 샐 수 있다.
  --fill-holes N  장애물로 완전히 둘러싸인 '모름' 영역(N 셀 이하)을 장애물로 채운다.
                  SLAM 지도에서 기둥은 둘레만 있고 속이 '모름'이라 속이 빈 고리가 된다.
"""
import argparse
import pathlib
import sys
from collections import deque

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from grid_map import load_map, save_map  # noqa: E402
from pgm_to_world import generate_world  # noqa: E402

FREE, OCCUPIED, UNKNOWN = 0, 100, -1
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))


def neighbors(gm, ix, iy, offsets):
    for dx, dy in offsets:
        jx, jy = ix + dx, iy + dy
        if gm.in_bounds(jx, jy):
            yield jx, jy


def seal_unknown(gm):
    """빈 곳과 8방향으로 맞닿은 '모름' 셀을 장애물로 바꾼다. 바뀐 셀 수를 돌려준다."""
    to_seal = []
    for iy in range(gm.height):
        for ix in range(gm.width):
            if gm.data[iy * gm.width + ix] == UNKNOWN and any(
                    gm.data[jy * gm.width + jx] == FREE for jx, jy in neighbors(gm, ix, iy, N8)):
                to_seal.append(iy * gm.width + ix)
    for i in to_seal:  # 한꺼번에 바꿔서 틈이 연쇄적으로 두꺼워지지 않게 한다.
        gm.data[i] = OCCUPIED
    return len(to_seal)


def fill_holes(gm, max_cells):
    """장애물로만 둘러싸인 작은 '모름' 영역을 장애물로 채운다. (채운 셀 수, 채운 영역 수)"""
    seen = bytearray(gm.width * gm.height)
    filled_cells = filled_regions = 0
    for sy in range(gm.height):
        for sx in range(gm.width):
            start = sy * gm.width + sx
            if gm.data[start] != UNKNOWN or seen[start]:
                continue
            region, queue = [], deque([(sx, sy)])
            seen[start] = 1
            enclosed = True              # 지도 가장자리나 빈 곳과 닿지 않아야 한다
            while queue:
                ix, iy = queue.popleft()
                region.append(iy * gm.width + ix)
                for dx, dy in N4:
                    jx, jy = ix + dx, iy + dy
                    if not gm.in_bounds(jx, jy):
                        enclosed = False
                        continue
                    v = gm.data[jy * gm.width + jx]
                    if v == FREE:
                        enclosed = False
                    elif v == UNKNOWN and not seen[jy * gm.width + jx]:
                        seen[jy * gm.width + jx] = 1
                        queue.append((jx, jy))
            if enclosed and len(region) <= max_cells:
                for i in region:
                    gm.data[i] = OCCUPIED
                filled_cells += len(region)
                filled_regions += 1
    return filled_cells, filled_regions


def best_start(gm):
    """장애물에서 가장 멀리 떨어진 빈 셀 (월드 좌표 x, y, 여유 거리 m). 로봇을 놓을 자리 추천용."""
    dist = [-1] * (gm.width * gm.height)
    queue = deque()
    for iy in range(gm.height):
        for ix in range(gm.width):
            if gm.data[iy * gm.width + ix] != FREE:
                dist[iy * gm.width + ix] = 0
                queue.append((ix, iy))
    while queue:
        ix, iy = queue.popleft()
        for jx, jy in neighbors(gm, ix, iy, N8):
            if dist[jy * gm.width + jx] < 0:
                dist[jy * gm.width + jx] = dist[iy * gm.width + ix] + 1
                queue.append((jx, jy))
    best = max((d, -abs(i % gm.width - gm.width / 2) - abs(i // gm.width - gm.height / 2), i)
               for i, d in enumerate(dist) if d > 0)
    ix, iy = best[2] % gm.width, best[2] // gm.width
    x, y = gm.cell_center(ix, iy)
    return x, y, best[0] * gm.resolution


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source_yaml')
    ap.add_argument('name', help='만들 지도/월드의 이름 (maps/<이름>.yaml, worlds/<이름>.sdf)')
    ap.add_argument('--seal-unknown', action='store_true')
    ap.add_argument('--fill-holes', type=int, default=0, metavar='N')
    ap.add_argument('--height', type=float, default=1.0, help='벽 높이 [m]')
    args = ap.parse_args()

    pkg_dir = pathlib.Path(__file__).resolve().parent.parent
    gm = load_map(args.source_yaml)
    count = lambda v: sum(1 for c in gm.data if c == v)  # noqa: E731
    print(f'원본: {gm.width}x{gm.height}, {gm.resolution} m/셀, 원점 ({gm.origin_x}, {gm.origin_y}), '
          f'장애물 {count(OCCUPIED)} / 빈 곳 {count(FREE)} / 모름 {count(UNKNOWN)}')

    if args.seal_unknown:
        print(f'틈 메우기: 모름 셀 {seal_unknown(gm)}개를 장애물로 바꿈')
    if args.fill_holes:
        cells, regions = fill_holes(gm, args.fill_holes)
        print(f'속 채우기: 둘러싸인 모름 영역 {regions}곳 ({cells}셀)을 장애물로 채움')

    save_map(gm, pkg_dir / 'maps', args.name)
    print(f'저장: maps/{args.name}.pgm, maps/{args.name}.yaml')
    generate_world(pkg_dir / 'maps' / f'{args.name}.yaml', pkg_dir / 'worlds' / f'{args.name}.sdf', args.height)

    x, y, clearance = best_start(gm)
    print(f'로봇 시작 위치 추천: x:={x:.2f} y:={y:.2f} (장애물까지 약 {clearance:.2f} m)')


if __name__ == '__main__':
    main()
