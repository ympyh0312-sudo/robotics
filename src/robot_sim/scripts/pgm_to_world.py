#!/usr/bin/env python3
"""지도(YAML + PGM)의 장애물 셀을 벽 상자로 세워 Gazebo 월드(SDF)를 만든다.

    python3 pgm_to_world.py maps/simple_room.yaml worlds/simple_room.sdf [--height 1.0]

월드를 직접 고치지 말고 지도(PGM)를 고친 뒤 이 스크립트를 다시 실행한다.
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from grid_map import load_map  # noqa: E402


def merge_rectangles(gm):
    """장애물 셀을 직사각형 몇 개로 합친다. 반환: [(ix0, iy0, 가로 셀 수, 세로 셀 수)]

    각 줄에서 연속된 장애물 구간(run)을 찾고, 바로 윗줄과 x 범위가 같으면 세로로 이어 붙인다.
    셀마다 상자를 만들면 상자가 수만 개가 되어 시뮬레이션이 느려진다.
    """
    rects, active = [], {}      # active: (ix0, nx) -> [iy0, 지금까지 쌓은 줄 수]
    for iy in range(gm.height):
        runs, ix = [], 0
        while ix < gm.width:
            if gm.is_occupied(ix, iy):
                start = ix
                while ix < gm.width and gm.is_occupied(ix, iy):
                    ix += 1
                runs.append((start, ix - start))
            else:
                ix += 1
        nxt = {}
        for run in runs:
            if run in active:
                iy0, ny = active.pop(run)
                nxt[run] = [iy0, ny + 1]
            else:
                nxt[run] = [iy, 1]
        rects.extend((r[0], v[0], r[1], v[1]) for r, v in active.items())
        active = nxt
    rects.extend((r[0], v[0], r[1], v[1]) for r, v in active.items())
    return rects


HEADER = """<?xml version="1.0" ?>
<!--
  {name}: 지도 {yaml} 에서 자동 생성한 월드. 직접 수정하지 말 것.
  지도(PGM)를 고친 뒤 scripts/pgm_to_world.py 를 다시 실행한다.
  좌표계는 지도의 map 프레임과 같다. (x 앞, y 왼쪽, z 위, 단위 m)
-->
<sdf version="1.9">
  <world name="{name}">

    <physics name="1ms" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>

    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.9 0.9 0.9 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <model name="ground_plane">
      <static>true</static>
      <pose>{cx:.3f} {cy:.3f} 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal><size>{gsize:.1f} {gsize:.1f}</size></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>{gsize:.1f} {gsize:.1f}</size></plane></geometry>
          <material><ambient>0.8 0.8 0.8 1</ambient><diffuse>0.8 0.8 0.8 1</diffuse></material>
        </visual>
      </link>
    </model>

    <model name="map_obstacles">
      <static>true</static>
"""

LINK = """      <link name="b{n}">
        <pose>{x:.3f} {y:.3f} {z:.3f} 0 0 0</pose>
        <collision name="collision"><geometry><box><size>{sx:.3f} {sy:.3f} {sz:.3f}</size></box></geometry></collision>
        <visual name="visual">
          <geometry><box><size>{sx:.3f} {sy:.3f} {sz:.3f}</size></box></geometry>
          <material><ambient>0.5 0.5 0.55 1</ambient><diffuse>0.5 0.5 0.55 1</diffuse></material>
        </visual>
      </link>
"""

FOOTER = """    </model>

  </world>
</sdf>
"""


def generate_world(map_yaml, world_sdf, height=1.0):
    """지도(YAML+PGM)에서 월드 SDF 를 만들어 world_sdf 에 저장한다."""
    gm = load_map(map_yaml)
    rects = merge_rectangles(gm)
    res = gm.resolution
    name = pathlib.Path(world_sdf).stem
    width_m, height_m = gm.width * res, gm.height * res

    parts = [HEADER.format(
        name=name, yaml=pathlib.Path(map_yaml).name,
        cx=gm.origin_x + width_m / 2, cy=gm.origin_y + height_m / 2,
        gsize=max(width_m, height_m) + 2.0)]
    for n, (ix0, iy0, nx, ny) in enumerate(rects):
        parts.append(LINK.format(
            n=n, x=gm.origin_x + (ix0 + nx / 2) * res, y=gm.origin_y + (iy0 + ny / 2) * res,
            z=height / 2, sx=nx * res, sy=ny * res, sz=height))
    parts.append(FOOTER)
    pathlib.Path(world_sdf).write_text(''.join(parts))

    occupied = sum(1 for v in gm.data if v == 100)
    print(f'{world_sdf}: 장애물 셀 {occupied}개 -> 상자 {len(rects)}개')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('map_yaml')
    ap.add_argument('world_sdf')
    ap.add_argument('--height', type=float, default=1.0, help='벽 높이 [m]')
    args = ap.parse_args()
    generate_world(args.map_yaml, args.world_sdf, args.height)


if __name__ == '__main__':
    main()
