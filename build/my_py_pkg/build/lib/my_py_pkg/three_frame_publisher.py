# base_link`, `camera_link`(앞 0.15m, 위 0.2m), `lidar_link`(앞 0.0m, 위 0.25m) 세 프레임을 가진 로봇을 만드세요. 모든 변환을 발행하고 `view_frames`와 RViz로 트리를 확인하세요.

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster
import tf_transformations

class StaticFramePublisher(Node):
    def __init__(self):
        super().__init__("three_static_frame_publisher")
        self.broadcaster_ = StaticTransformBroadcaster(self)
        self.send_static_transform()

    def send_static_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "base_link"
        t.child_frame_id = "lidar_link"
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.25
        q = tf_transformations.quaternion_from_euler(0, 0, 0)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        self.broadcaster_.sendTransform(t)

        p = TransformStamped()
        p.header.stamp = self.get_clock().now().to_msg()
        p.header.frame_id = "base_link"
        p.child_frame_id = "camera_link"
        p.transform.translation.x = 0.15
        p.transform.translation.y = 0.0
        p.transform.translation.z = 0.2
        a = tf_transformations.quaternion_from_euler(0, 0, 0)
        p.transform.rotation.x = a[0]
        p.transform.rotation.y = a[1]
        p.transform.rotation.z = a[2]
        p.transform.rotation.w = a[3]
        self.broadcaster_.sendTransform(p)

def main(args = None):
    rclpy.init(args = args)
    node = StaticFramePublisher()
    rclpy.spin(node)
    rclpy.shutdown()
