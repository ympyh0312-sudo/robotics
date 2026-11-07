import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class HelloNode(Node):

    def __init__(self):
        super().__init__('planner_py_hello')
        self.count = 0
        self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.count += 1
        self.get_logger().info(f'planner_py alive: {self.count}')


def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
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
