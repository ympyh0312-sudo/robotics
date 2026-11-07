#!/usr/bin/env python3
"""배치 파일(layouts/*.yaml)에서 지도(PGM+YAML)와 Gazebo 월드(SDF)를 한 번에 만든다.

    python3 make_map.py layouts/large_room.yaml

결과: maps/<이름>.pgm, maps/<이름>.yaml, worlds/<이름>.sdf   (<이름>은 배치 파일 이름)
새 파일이 생기면 `colcon build` 를 한 번 다시 해야 ros2 launch 가 찾는다.
검정(0)이 장애물, 흰색(254)이 빈 곳이다. 직접 만든 PGM 을 쓰려면 pgm_to_world.py 만 실행한다.
"""
import math
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from pgm_to_world import generate_world  # noqa: E402

FREE, OCCUPIED = 254, 0


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    layout_path = pathlib.Path(sys.argv[1]).resolve()
    name = layout_path.stem
    pkg_dir = layout_path.parent.parent
    layout = yaml.safe_load(layout_path.read_text())

    res = float(layout['resolution'])
    size_x, size_y = layout['size']
    room_x, room_y = layout['room']
    t = float(layout.get('wall_thickness', 0.2))
    if room_x + 2 * t > size_x or room_y + 2 * t > size_y:
        sys.exit('오류: size 가 방과 벽보다 작다')

    # (중심 x, 중심 y, 가로, 세로): 방 안쪽 면이 ±room/2 가 되도록 벽을 바깥에 둔다.
    rects = [
        (0.0, room_y / 2 + t / 2, room_x + 2 * t, t), (0.0, -room_y / 2 - t / 2, room_x + 2 * t, t),
        (room_x / 2 + t / 2, 0.0, t, room_y + 2 * t), (-room_x / 2 - t / 2, 0.0, t, room_y + 2 * t),
    ] + [tuple(b) for b in layout.get('boxes', [])]
    disks = [tuple(d) for d in layout.get('disks', [])]

    def occupied(x, y):
        for cx, cy, sx, sy in rects:
            if abs(x - cx) <= sx / 2 and abs(y - cy) <= sy / 2:
                return True
        return any(math.hypot(x - cx, y - cy) <= r for cx, cy, r in disks)

    width, height = round(size_x / res), round(size_y / res)
    origin = (-size_x / 2, -size_y / 2)

    pixels = bytearray()
    for j in range(height):                  # j: 이미지의 줄 번호, 위쪽이 0
        y = origin[1] + (height - 1 - j + 0.5) * res
        for i in range(width):
            x = origin[0] + (i + 0.5) * res
            pixels.append(OCCUPIED if occupied(x, y) else FREE)

    maps_dir, worlds_dir = pkg_dir / 'maps', pkg_dir / 'worlds'
    maps_dir.mkdir(exist_ok=True)
    worlds_dir.mkdir(exist_ok=True)
    (maps_dir / f'{name}.pgm').write_bytes(f'P5\n{width} {height}\n255\n'.encode() + bytes(pixels))
    (maps_dir / f'{name}.yaml').write_text(
        f'image: {name}.pgm\n'
        'mode: trinary\n'
        f'resolution: {res}\n'
        f'origin: [{origin[0]}, {origin[1]}, 0.0]\n'
        'negate: 0\n'
        'occupied_thresh: 0.65\n'
        'free_thresh: 0.25\n')
    print(f'{maps_dir / name}.pgm ({width}x{height}, {res} m/cell)')
    generate_world(maps_dir / f'{name}.yaml', worlds_dir / f'{name}.sdf')


if __name__ == '__main__':
    main()
