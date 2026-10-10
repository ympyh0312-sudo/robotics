from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value = 'my_robot',
        description = 'Name of the robot'
    )

    news_robot_station_node = Node(
        package = 'my_py_pkg',
        executable = 'news_robot_station',
        name = 'news_robot_station',
        parameters = [{'robot_name': LaunchConfiguration('robot_name')}],
        remappings = [('/robot_news', '/robot_news_v2')]
    )

    smartphone_node = Node(
        package = 'my_py_pkg',
        executable = 'smartphone',
        name = 'smartphone',
        remappings = [('/robot_news', '/robot_news_v2')]
    )

    return LaunchDescription([
        robot_name_arg,
        news_robot_station_node,
        smartphone_node
    ])