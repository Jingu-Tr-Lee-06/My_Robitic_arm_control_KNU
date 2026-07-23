from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 퍼블리셔 노드 실행 설정
        Node(
            package='my_first_pkg',
            executable='my_publisher',
            name='publisher_node'
        ),
        # 구독자 노드 실행 설정
        Node(
            package='my_first_pkg',
            executable='my_subscriber',
            name='subscriber_node'
        )
    ])