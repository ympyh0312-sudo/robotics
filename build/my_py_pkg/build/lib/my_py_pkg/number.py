import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class number(Node):
    def __init__(self):
        super().__init__("number")
        self.pub_ = self.create_publisher(Int64, "/number_count", 10)
        self.timers_ = self.create_timer(1.0, self.publish_news)
        self.get_logger().info("robot news station started")
        self.counter_ = 0

    def publish_news(self):
        msg = Int64()
        msg.data = self.counter_
        self.pub_.publish(msg)

def main(args = None):
    rclpy.init(args = args)
    node = number()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
