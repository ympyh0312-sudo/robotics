import rclpy
from rclpy.node import Node

class MyfirstNode(Node):
    def __init__(self):
        super().__init__("my_first_node")
        self.get_logger().info("Hello from my first ROS 2 node")
        self.counter = 0
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.counter += 1
        self.get_logger().info(f"timer fired{self.counter} times")

def main(args = None):
    rclpy.init(args = args)
    node = MyfirstNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

