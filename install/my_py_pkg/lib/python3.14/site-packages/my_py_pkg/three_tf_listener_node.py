# base_link`, `camera_link`(앞 0.15m, 위 0.2m), `lidar_link`(앞 0.0m, 위 0.25m) 세 프레임을 가진 로봇을 만드세요. 모든 변환을 발행하고 `view_frames`와 RViz로 트리를 확인하세요.

import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener

class TFListenerNode(Node):
    def __init__(self):
        super().__init__("tf_listener")
        self.tf_buffer_ = Buffer()
        self.tf_listener_ = TransformListener(self.tf_buffer_, self)
        self.timer_ = self.create_timer(0.5, self.lookup_transform)

    def lookup_transform(self):
        try:
            t = self.tf_buffer_.lookup_transform(
                "base_link", "lidar_link", rclpy.time.Time())
            self.get_logger().info(
                f"lidar_link is at x = {t.transform.translation.x:.2f} "
                f"relative to base_link"
            )

        except Exception as e:
            self.get_logger().warning(str(e))

def main(args = None):
    rclpy.init(args = args)
    node = TFListenerNode()
    rclpy.spin(node)
    rclpy.shutdown()