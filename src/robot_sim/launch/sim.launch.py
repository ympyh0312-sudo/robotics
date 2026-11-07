"""Gazebo 월드 + 로봇 + ROS bridge + TF + RViz2 를 한 번에 실행한다.

    ros2 launch robot_sim sim.launch.py
    ros2 launch robot_sim sim.launch.py map:=simple_room
    ros2 launch robot_sim sim.launch.py headless:=true rviz:=false
    ros2 launch robot_sim sim.launch.py x:=2.0 y:=-3.0 yaw:=1.57
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('robot_sim')

    map_name = LaunchConfiguration('map')
    headless = LaunchConfiguration('headless')
    rviz = LaunchConfiguration('rviz')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    yaw = LaunchConfiguration('yaw')

    # 같은 이름의 월드와 지도를 짝으로 쓴다: worlds/<map>.sdf, maps/<map>.yaml
    world_path = PathJoinSubstitution([pkg, 'worlds', [map_name, '.sdf']])
    map_yaml = PathJoinSubstitution([pkg, 'maps', [map_name, '.yaml']])
    robot_path = PathJoinSubstitution([pkg, 'models', 'diff_bot.sdf'])
    bridge_cfg = PathJoinSubstitution([pkg, 'config', 'bridge.yaml'])
    rviz_cfg = PathJoinSubstitution([pkg, 'rviz', 'sim.rviz'])

    sim_time = {'use_sim_time': True}

    # -r: 시작하자마자 실행, -s: GUI 없이 서버만, --headless-rendering: 화면 없이 센서 렌더링
    gz_args = [
        world_path, ' -r',
        PythonExpression(["' -s --headless-rendering' if '", headless, "' == 'true' else ''"]),
    ]
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={'gz_args': gz_args}.items(),
    )

    spawn_robot = Node(
        package='ros_gz_sim', executable='create', output='screen',
        arguments=['-file', robot_path, '-name', 'diff_bot',
                   '-x', x, '-y', y, '-z', '0.02', '-Y', yaw],
    )

    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge', output='screen',
        parameters=[{'config_file': bridge_cfg}],
    )

    # map -> odom: 오도메트리는 로봇이 생성된 자리에서 0 으로 시작하므로 생성 위치를 그대로 쓴다.
    map_to_odom = Node(
        package='tf2_ros', executable='static_transform_publisher',
        name='map_to_odom', parameters=[sim_time],
        arguments=['--x', x, '--y', y, '--yaw', yaw,
                   '--frame-id', 'map', '--child-frame-id', 'odom'],
    )

    # base_link -> lidar_link: diff_bot.sdf 의 센서 위치와 같아야 한다.
    base_to_lidar = Node(
        package='tf2_ros', executable='static_transform_publisher',
        name='base_to_lidar', parameters=[sim_time],
        arguments=['--x', '0.1', '--z', '0.16',
                   '--frame-id', 'base_link', '--child-frame-id', 'lidar_link'],
    )

    # /map: 월드를 만든 것과 같은 지도 파일을 플래너가 쓸 수 있게 발행한다.
    map_publisher = Node(
        package='robot_sim', executable='map_publisher.py', output='screen',
        parameters=[{'map_yaml': map_yaml}, sim_time],
    )

    rviz2 = Node(
        package='rviz2', executable='rviz2', output='log',
        arguments=['-d', rviz_cfg], parameters=[sim_time],
        condition=IfCondition(rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument('map', default_value='simple_room',
                              description='지도 이름. worlds/<이름>.sdf 와 maps/<이름>.yaml 을 쓴다'),
        DeclareLaunchArgument('headless', default_value='false',
                              description='true 이면 Gazebo GUI 없이 서버만 실행'),
        DeclareLaunchArgument('rviz', default_value='true', description='RViz2 실행 여부'),
        DeclareLaunchArgument('x', default_value='-3.0', description='로봇 생성 위치 x [m]'),
        DeclareLaunchArgument('y', default_value='-3.0', description='로봇 생성 위치 y [m]'),
        DeclareLaunchArgument('yaw', default_value='0.0', description='로봇 생성 방향 [rad]'),
        gz_sim, spawn_robot, bridge, map_to_odom, base_to_lidar, map_publisher, rviz2,
    ])
