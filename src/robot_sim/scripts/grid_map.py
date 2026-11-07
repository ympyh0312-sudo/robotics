"""ROS map_server 형식(YAML + PGM)의 점유 격자 지도를 읽는다.

좌표 규약 (플래너를 만들 때도 똑같이 쓴다):
  - 셀 (ix, iy): ix 는 x 방향(오른쪽), iy 는 y 방향(위쪽)으로 커진다.
  - data[iy * width + ix], 값은 0=빈 곳, 100=장애물, -1=모름. (nav_msgs/OccupancyGrid 와 같다)
  - 셀 (0, 0) 의 왼쪽 아래 모서리가 지도 원점 (origin_x, origin_y) 이다.
  - 이미지 파일은 위쪽 줄이 먼저 저장되어 있어서, 읽을 때 위아래를 뒤집는다.
    이것을 빼먹으면 지도가 상하로 뒤집힌다.
"""
import math
import pathlib
from dataclasses import dataclass

import yaml


@dataclass
class GridMap:
    width: int
    height: int
    resolution: float
    origin_x: float
    origin_y: float
    data: list

    def in_bounds(self, ix, iy):
        return 0 <= ix < self.width and 0 <= iy < self.height

    def is_occupied(self, ix, iy):
        return self.data[iy * self.width + ix] == 100

    def cell_center(self, ix, iy):
        """셀 중심의 월드 좌표 (x, y) [m]"""
        return (self.origin_x + (ix + 0.5) * self.resolution,
                self.origin_y + (iy + 0.5) * self.resolution)

    def world_to_cell(self, x, y):
        """월드 좌표가 속한 셀 (ix, iy). 지도 밖이면 범위를 벗어난 값이 나온다."""
        return (math.floor((x - self.origin_x) / self.resolution),
                math.floor((y - self.origin_y) / self.resolution))


def read_pgm(path):
    """바이너리 PGM(P5)을 읽어 (width, height, 픽셀 bytes) 를 돌려준다. 위쪽 줄이 먼저다."""
    raw = pathlib.Path(path).read_bytes()
    tokens, pos = [], 0
    while len(tokens) < 4:
        while raw[pos:pos + 1].isspace():
            pos += 1
        if raw[pos:pos + 1] == b'#':
            while raw[pos:pos + 1] != b'\n':
                pos += 1
            continue
        start = pos
        while not raw[pos:pos + 1].isspace():
            pos += 1
        tokens.append(raw[start:pos])
    pos += 1  # 헤더 뒤 공백 한 칸
    magic, width, height, maxval = tokens[0], int(tokens[1]), int(tokens[2]), int(tokens[3])
    if magic != b'P5' or maxval != 255:
        raise ValueError(f'{path}: 8비트 바이너리 PGM(P5)만 지원한다 (magic={magic}, maxval={maxval})')
    pixels = raw[pos:pos + width * height]
    if len(pixels) != width * height:
        raise ValueError(f'{path}: 픽셀 수가 헤더와 다르다')
    return width, height, pixels


def load_map(yaml_path):
    yaml_path = pathlib.Path(yaml_path)
    meta = yaml.safe_load(yaml_path.read_text())
    origin = meta['origin']
    if abs(origin[2]) > 1e-9:
        raise ValueError('origin 의 yaw 는 0 만 지원한다')
    negate = int(meta.get('negate', 0))
    occupied_thresh = float(meta.get('occupied_thresh', 0.65))
    free_thresh = float(meta.get('free_thresh', 0.25))

    width, height, pixels = read_pgm(yaml_path.parent / meta['image'])

    def classify(pix):
        p = pix / 255.0 if negate else (255 - pix) / 255.0  # 0 에 가까우면 빈 곳
        if p > occupied_thresh:
            return 100
        if p < free_thresh:
            return 0
        return -1

    data = []
    for iy in range(height):
        j = height - 1 - iy  # 이미지의 줄 번호 (위에서부터)
        data.extend(classify(v) for v in pixels[j * width:(j + 1) * width])
    return GridMap(width, height, float(meta['resolution']), float(origin[0]), float(origin[1]), data)
