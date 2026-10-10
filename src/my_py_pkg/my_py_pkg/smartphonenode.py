import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SmartphoneNode(Node):
    def __init__(self):
        super().__init__("smartphone")
        self.sub_ = self.create_subscription(String, "/robot_news", self.callback_robot_news, 10)
        self.get_logger().info("Smartphone node started")

    def callback_robot_news(self, msg: String):
        self.get_logger().info(f"Received: {msg.data}")

def main(args = None):
    rclpy.init(args = args)
    node = SmartphoneNode()
    rclpy.spin(node)
    rclpy.shutdown()

    