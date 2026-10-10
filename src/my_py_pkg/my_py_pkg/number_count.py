import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class numbernode(Node):
    def __init__(self):
        super().__init__("number_count")
        self.pub_ = self.create_publisher(Int64, "/number_count", 10)
        self.sub_ = self.create_subscription(Int64, "/number", self.callback_number_count, 10)
        self.counter_ = 0

    def callback_number_count(self, msg: Int64):
        self.get_logger().info(f"Received: {msg.data}")
        self.counter_ += msg.data

def main(args = None):
    rclpy.init(args = args)
    node = numbernode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main__":
    main()
