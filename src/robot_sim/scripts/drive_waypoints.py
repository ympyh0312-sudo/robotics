import math
import sys

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

ARRIVE_M = 0.15
TURN_ONLY_RAD = 0.4
MAX_SPEED = 0.3
MAX_TURN = 0.6
TIMEOUT_S = 600.0


def wrap(angle):
    return math.atan2(math.sin(angle), math.cos(angle))


def clip(value, limit):
    return max(-limit, min(limit, value))


class Driver(Node):

    def __init__(self, waypoints):
        sim_time = Parameter('use_sim_time', Parameter.Type.BOOL, True)
        super().__init__('drive_waypoints', parameter_overrides=[sim_time])
        self.waypoints = waypoints
        self.index = 0
        self.pose = None
        self.start = self.get_clock().now()
        self.finished = False
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(Odometry, '/odom', self.on_odom, 10)
        self.create_timer(0.05, self.step)

    def on_odom(self, msg):
        q = msg.pose.pose.orientation
        self.pose = (msg.pose.pose.position.x, msg.pose.pose.position.y,
                     2.0 * math.atan2(q.z, q.w))

    def stop(self, reason):
        self.pub.publish(Twist())
        self.get_logger().info(reason)
        self.finished = True

    def step(self):
        if self.pose is None or self.finished:
            return
        if (self.get_clock().now() - self.start).nanoseconds * 1e-9 > TIMEOUT_S:
            return self.stop('timeout')
        if self.index >= len(self.waypoints):
            return self.stop('all waypoints reached')

        x, y, yaw = self.pose
        tx, ty = self.waypoints[self.index]
        distance = math.hypot(tx - x, ty - y)
        if distance < ARRIVE_M:
            self.get_logger().info(f'reached waypoint {self.index + 1}/{len(self.waypoints)} '
                                   f'({tx:.1f}, {ty:.1f})')
            self.index += 1
            return
        error = wrap(math.atan2(ty - y, tx - x) - yaw)
        cmd = Twist()
        cmd.angular.z = clip(1.5 * error, MAX_TURN)
        if abs(error) < TURN_ONLY_RAD:
            cmd.linear.x = min(MAX_SPEED, 0.8 * distance)
        self.pub.publish(cmd)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    waypoints = [tuple(float(v) for v in arg.split(',')) for arg in sys.argv[1:]]
    rclpy.init()
    node = Driver(waypoints)
    while rclpy.ok() and not node.finished:
        rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
