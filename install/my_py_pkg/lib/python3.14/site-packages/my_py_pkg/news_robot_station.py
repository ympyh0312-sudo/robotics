import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class news_robot_station(Node):
    def __init__(self):
        super().__init__("news_robot_station")
        self.declare_parameter("robot_name", "my_robot")
        self.robot_name_ = self.get_parameter("robot_name").value
        self.pub_ = self.create_publisher(String, "/robot_news", 10)
        self.timers_ = self.create_timer(0.5, self.publish_news)
        self.get_logger().info("robot news station started")

    def publish_news(self):
        msg = String()
        msg.data = "Breaking news from " + self.robot_name_
        self.pub_.publish(msg)

def main(args = None):
    rclpy.init(args = args)
    node = news_robot_station()
    rclpy.spin(node)
    rclpy.shutdown()
