import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_name = 'my_first_pkg'
    pkg_dir = get_package_share_directory(pkg_name)
    urdf_file = os.path.join(pkg_dir, 'urdf', 'simple_arm.urdf')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    ros_gz_sim_dir = get_package_share_directory('ros_gz_sim')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_dir, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': 'empty.sdf -r'}.items()
    )

    return LaunchDescription([
        # 1. Gazebo 시뮬레이터 실행
        gazebo_launch,

        # 2. 로봇 상태 퍼블리셔
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
        ),

        # 3. Gazebo 안에 로봇 스폰
        Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_simple_arm',
            arguments=['-topic', 'robot_description', '-name', 'simple_arm', '-z', '0.2'],
            output='screen'
        ),

        # 4. RViz 및 관절 제어 GUI
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        ),

        # 5. 패키지 기본 테스트용 토픽 노드
        Node(
            package='my_first_pkg',
            executable='my_publisher',
            name='publisher_node',
            output='screen'
        ),
        Node(
            package='my_first_pkg',
            executable='my_subscriber',
            name='subscriber_node',
            output='screen'
        ),
    ])
