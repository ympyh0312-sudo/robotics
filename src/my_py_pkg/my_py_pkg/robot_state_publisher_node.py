import rclpy
from rclpy.node import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

robot_description = ParameterValue(
    Command(["xacro", "/home/yanghee/ros2_course_ws/src/my_robot_description/my_robot.urdf"]),
    value_type = str
)

robot_state_publisher_node = Node(
    package = "robot_state_publisher",
    executable = "robot_state_publisher",
    parameter = [{"robot_description : robot_description"}]
)