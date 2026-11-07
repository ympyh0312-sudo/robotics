#!/usr/bin/env python3
"""지도(YAML + PGM)를 읽어 /map (nav_msgs/OccupancyGrid) 으로 한 번 발행한다.

nav2_map_server 와 같은 역할의 간단한 버전이다. 지도는 바뀌지 않으므로 QoS 를
transient_local 로 두어, 나중에 시작한 노드(RViz2, 플래너)도 마지막 지도를 받게 한다.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import rclpy  # noqa: E402
from grid_map import load_map  # noqa: E402
from nav_msgs.msg import OccupancyGrid  # noqa: E402
from rclpy.executors import ExternalShutdownException  # noqa: E402
from rclpy.node import Node  # noqa: E402
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy  # noqa: E402


class MapPublisher(Node):

    def __init__(self):
        super().__init__('map_publisher')
        self.declare_parameter('map_yaml', '')
        self.declare_parameter('frame_id', 'map')
        map_yaml = self.get_parameter('map_yaml').value
        if not map_yaml:
            raise RuntimeError('map_yaml 파라미터가 필요하다')

        gm = load_map(map_yaml)
        msg = OccupancyGrid()
        msg.header.frame_id = self.get_parameter('frame_id').value
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.info.resolution = gm.resolution
        msg.info.width = gm.width
        msg.info.height = gm.height
        msg.info.origin.position.x = gm.origin_x
        msg.info.origin.position.y = gm.origin_y
        msg.info.origin.orientation.w = 1.0
        msg.data = gm.data

        qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL,
                         reliability=ReliabilityPolicy.RELIABLE)
        self.pub = self.create_publisher(OccupancyGrid, '/map', qos)
        self.pub.publish(msg)
        occupied = sum(1 for v in gm.data if v == 100)
        self.get_logger().info(
            f'/map 발행: {gm.width}x{gm.height} 셀, {gm.resolution} m/셀, '
            f'{gm.width * gm.resolution:.1f}x{gm.height * gm.resolution:.1f} m, '
            f'장애물 셀 {occupied}개, 원점 ({gm.origin_x}, {gm.origin_y})')


def main(args=None):
    rclpy.init(args=args)
    node = MapPublisher()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
