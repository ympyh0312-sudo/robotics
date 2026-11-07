"""
Global planner node: /map and /goal_pose in, /plan out.

    ros2 launch planner_py planner.launch.py algorithm:=astar

Send a goal from RViz2 with the "2D Goal Pose" button. The start is the current pose of the
robot, taken from the TF tree (map -> base_link).
"""
from array import array
import math
import time

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid, Path
from planner_py.astar import astar
from planner_py.dijkstra import dijkstra
from planner_py.grid import Grid, make_grid_msg
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from rclpy.time import Time
import tf2_ros

ALGORITHMS = {'dijkstra': dijkstra, 'astar': astar}

# The last message is kept for nodes (and RViz2 displays) that start later.
LATCHED = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL,
                     reliability=ReliabilityPolicy.RELIABLE)
VISITED_VALUE = 60


def yaw_to_quaternion(yaw):
    return math.sin(yaw / 2.0), math.cos(yaw / 2.0)  # (z, w)


class PlannerNode(Node):

    def __init__(self):
        super().__init__('planner')
        self.declare_parameter('algorithm', 'astar')
        self.declare_parameter('robot_radius', 0.25)
        self.declare_parameter('unknown_is_blocked', True)
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('base_frame', 'base_link')

        self.grid = None
        self.tf_buffer = tf2_ros.Buffer()
        tf2_ros.TransformListener(self.tf_buffer, self)

        self.plan_pub = self.create_publisher(Path, '/plan', LATCHED)
        self.visited_pub = self.create_publisher(OccupancyGrid, '/planner/visited', LATCHED)
        self.inflated_pub = self.create_publisher(OccupancyGrid, '/planner/inflated_map', LATCHED)
        self.create_subscription(OccupancyGrid, '/map', self.on_map, LATCHED)
        self.create_subscription(PoseStamped, '/goal_pose', self.on_goal, 10)
        self.get_logger().info(
            f"planner ready: algorithm={self.get_parameter('algorithm').value}. "
            'Waiting for /map, then send a goal with 2D Goal Pose.')

    def on_map(self, msg):
        radius = self.get_parameter('robot_radius').value
        t0 = time.perf_counter()
        self.grid = Grid.from_occupancy_grid(
            msg, radius, self.get_parameter('unknown_is_blocked').value)
        blocked = sum(self.grid.blocked)
        self.get_logger().info(
            f'map received: {msg.info.width}x{msg.info.height} cells, '
            f'{msg.info.resolution} m/cell. Inflated by {radius} m: {blocked} blocked cells '
            f'({(time.perf_counter() - t0) * 1000:.0f} ms)')
        data = array('b', bytearray(100 if b else 0 for b in self.grid.blocked))
        self.inflated_pub.publish(
            make_grid_msg(self.grid, data, msg.header.frame_id, self.get_clock().now().to_msg()))

    def on_goal(self, msg):
        log = self.get_logger()
        if self.grid is None:
            log.warning('No map yet. Is map_publisher running?')
            return
        map_frame = self.get_parameter('map_frame').value
        if msg.header.frame_id != map_frame:
            log.warning(f"Goal is in frame '{msg.header.frame_id}', expected '{map_frame}'. "
                        'Set the RViz2 Fixed Frame to map.')
            return

        try:
            tf = self.tf_buffer.lookup_transform(
                map_frame, self.get_parameter('base_frame').value, Time())
        except tf2_ros.TransformException as e:
            log.warning(f'Cannot get the robot pose: {e}')
            return
        start = self.grid.world_to_cell(tf.transform.translation.x, tf.transform.translation.y)
        goal = self.grid.world_to_cell(msg.pose.position.x, msg.pose.position.y)

        if not self.grid.in_bounds(*goal):
            return self.fail(f'goal {goal} is outside the map')
        if not self.grid.is_free(*goal):
            return self.fail(f'goal {goal} is inside an obstacle or too close to one '
                             '(within the robot radius). Pick a point farther from the walls')
        if not self.grid.is_free(*start):
            return self.fail(f'start {start} is blocked (the robot is closer to a wall than '
                             'robot_radius). Move the robot away from the wall')

        name = self.get_parameter('algorithm').value
        algorithm = ALGORITHMS.get(name)
        if algorithm is None:
            return self.fail(f"unknown algorithm '{name}'. Choose from {sorted(ALGORITHMS)}")

        t0 = time.perf_counter()
        try:
            result = algorithm(self.grid, start, goal)
        except NotImplementedError as e:
            return self.fail(f'{name} is not implemented yet: {e}')
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        stamp = self.get_clock().now().to_msg()
        self.publish_visited(result.visited if result else [], stamp)
        if result is None:
            return self.fail(f'[{name}] no path from {start} to {goal} '
                             f'({elapsed_ms:.1f} ms). Is the goal in a closed-off area?')

        self.plan_pub.publish(self.to_path(result.path, msg, stamp))
        res = self.grid.resolution
        log.info(f'[{name}] start {start} -> goal {goal}: {len(result.path)} cells, '
                 f'length {result.cost * res:.2f} m, expanded {result.expanded} cells, '
                 f'{elapsed_ms:.1f} ms')

    def fail(self, reason):
        """Log why planning failed and clear the old path from RViz2."""
        self.get_logger().warning(f'Planning failed: {reason}')
        empty = Path()
        empty.header.frame_id = self.get_parameter('map_frame').value
        empty.header.stamp = self.get_clock().now().to_msg()
        self.plan_pub.publish(empty)

    def to_path(self, cells, goal_msg, stamp):
        path = Path()
        path.header.frame_id = self.get_parameter('map_frame').value
        path.header.stamp = stamp
        points = [self.grid.cell_to_world(ix, iy) for ix, iy in cells]
        for i, (x, y) in enumerate(points):
            pose = PoseStamped()
            pose.header = path.header
            pose.pose.position.x, pose.pose.position.y = x, y
            if i + 1 < len(points):
                nx, ny = points[i + 1]
                pose.pose.orientation.z, pose.pose.orientation.w = yaw_to_quaternion(
                    math.atan2(ny - y, nx - x))
            else:
                pose.pose.orientation = goal_msg.pose.orientation
            path.poses.append(pose)
        return path

    def publish_visited(self, cells, stamp):
        data = bytearray(self.grid.width * self.grid.height)
        for ix, iy in cells:
            data[iy * self.grid.width + ix] = VISITED_VALUE
        frame = self.get_parameter('map_frame').value
        self.visited_pub.publish(make_grid_msg(self.grid, array('b', data), frame, stamp))


def main(args=None):
    rclpy.init(args=args)
    node = PlannerNode()
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
