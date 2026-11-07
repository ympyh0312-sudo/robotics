import math
import pathlib
import sys
import time

from grid_map import load_map
from nav_msgs.msg import OccupancyGrid
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from rclpy.time import Time
from sensor_msgs.msg import LaserScan
import tf2_ros

TOLERANCE_M = 0.06
MIN_FRACTION = 0.99
MAX_ERROR_M = 0.10


def distance_to_obstacle(gm, px, py):
    """Return the distance [m] from a point to the nearest obstacle cell (square)."""
    ix, iy = gm.world_to_cell(px, py)
    best = 9.9
    for jy in range(iy - 4, iy + 5):
        for jx in range(ix - 4, ix + 5):
            if gm.in_bounds(jx, jy) and gm.is_occupied(jx, jy):
                cx, cy = gm.cell_center(jx, jy)
                dx = max(abs(px - cx) - gm.resolution / 2, 0.0)
                dy = max(abs(py - cy) - gm.resolution / 2, 0.0)
                best = min(best, math.hypot(dx, dy))
    return best


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    map_yaml = pathlib.Path(__file__).resolve().parent.parent / 'maps' / f'{sys.argv[1]}.yaml'
    gm = load_map(map_yaml)

    rclpy.init()
    node = Node('check_map_lidar',
                parameter_overrides=[Parameter('use_sim_time', Parameter.Type.BOOL, True)])
    buffer = tf2_ros.Buffer()
    tf2_ros.TransformListener(buffer, node)
    got = {}
    node.create_subscription(LaserScan, '/scan', lambda m: got.setdefault('scan', m), 10)
    node.create_subscription(
        OccupancyGrid, '/map', lambda m: got.setdefault('map', m),
        QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL,
                   reliability=ReliabilityPolicy.RELIABLE))

    transform = None
    deadline = time.time() + 25.0
    while time.time() < deadline and transform is None:
        rclpy.spin_once(node, timeout_sec=0.2)
        if 'scan' in got and 'map' in got:
            try:
                transform = buffer.lookup_transform('map', 'lidar_link', Time())
            except tf2_ros.TransformException:
                pass
    if transform is None:
        print('FAIL: did not receive /scan, /map and the TF chain', sorted(got))
        sys.exit(1)

    published = got['map']
    same_map = (list(published.data) == gm.data
                and (published.info.width, published.info.height) == (gm.width, gm.height))
    print(f'/map matches maps/{sys.argv[1]}.yaml: {same_map} '
          f'({published.info.width}x{published.info.height})')

    q = transform.transform.rotation
    yaw = 2.0 * math.atan2(q.z, q.w)
    tx, ty = transform.transform.translation.x, transform.transform.translation.y
    scan = got['scan']
    errors = []
    for i, r in enumerate(scan.ranges):
        if not scan.range_min < r < scan.range_max - 0.01:
            continue
        angle = scan.angle_min + i * scan.angle_increment
        lx, ly = r * math.cos(angle), r * math.sin(angle)
        px = tx + lx * math.cos(yaw) - ly * math.sin(yaw)
        py = ty + lx * math.sin(yaw) + ly * math.cos(yaw)
        errors.append(distance_to_obstacle(gm, px, py))
    rclpy.shutdown()

    if not errors:
        print('FAIL: no valid LiDAR hits')
        sys.exit(1)
    errors.sort()
    within = sum(e <= TOLERANCE_M for e in errors) / len(errors)
    print(f'lidar at map ({tx:.2f}, {ty:.2f}), yaw {yaw:.2f} rad, '
          f'{len(errors)} valid hits of {len(scan.ranges)} beams')
    print(f'hits within {TOLERANCE_M} m of an obstacle cell: {100 * within:.1f}% '
          f'(median {errors[len(errors) // 2]:.3f} m, max {errors[-1]:.3f} m)')
    ok = same_map and within >= MIN_FRACTION and errors[-1] <= MAX_ERROR_M
    print('PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
