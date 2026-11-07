"""
Start the global planner node.

    ros2 launch planner_py planner.launch.py
    ros2 launch planner_py planner.launch.py algorithm:=dijkstra robot_radius:=0.3
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('algorithm', default_value='astar',
                              description='astar or dijkstra'),
        DeclareLaunchArgument('robot_radius', default_value='0.25',
                              description='Obstacles are inflated by this radius [m]'),
        Node(
            package='planner_py', executable='planner_node', name='planner', output='screen',
            parameters=[{
                'use_sim_time': True,
                'algorithm': LaunchConfiguration('algorithm'),
                'robot_radius': LaunchConfiguration('robot_radius'),
            }],
        ),
    ])
