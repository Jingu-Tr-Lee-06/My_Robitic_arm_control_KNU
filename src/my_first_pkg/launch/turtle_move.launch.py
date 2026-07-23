from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Turtlesim 시뮬레이터 노드 실행
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),
        # 2. 앞서 작성한 파이썬 거북이 제어 노드 실행
        Node(
            package='my_first_pkg',
            executable='move_turtle',
            name='move_turtle_node'
        )
    ])