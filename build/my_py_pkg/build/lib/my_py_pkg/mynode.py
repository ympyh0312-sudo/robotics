import rclpy
from rclpy.node import Node


class Mynode(Node):
    def __init__(self):
        super().__init__('mynode')
        self.declare_parameter('robot_name', 'my_robot')
        self.declare_parameter('move_speed', 1.0)
        name = self.get_parameter('robot_name').value
        speed = self.get_parameter('move_speed').value
        self.get_logger().info(f'Robot: {name}, Speed: {speed}')


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Mynode())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
