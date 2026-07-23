import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_first_pkg')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'simple_arm.urdf')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # 1. URDF 로봇 구조 및 TF를 계산하여 퍼블리시하는 노드
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}]
        ),
        # 2. RViz2에서 관절 상태를 조작할 수 있는 GUI 슬라이더 노드
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        # 3. RViz2 3D 시각화 도구 실행
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2'
        )
    ])