import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import random

class RandomManipulatorMove(Node):
    def __init__(self):
        super().__init__('random_manipulator_move')
        
        # ROS 2 control arm_controller 토픽 퍼블리셔 생성
        self.publisher = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        
        # 2.5초마다 랜덤 위치 전송
        self.timer = self.create_timer(2.5, self.send_random_joint_goal)
        self.get_logger().info('🎲 로봇 팔 랜덤 제어 노드가 시작되었습니다!')

    def send_random_joint_goal(self):
        msg = JointTrajectory()
        msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
        
        point = JointTrajectoryPoint()
        
        # 안전한 각 관절별 라디안(rad) 범위 내 랜덤값 생성
        j1 = random.uniform(-0.8, 0.8)   # 좌우 회전 (Joint 1)
        j2 = random.uniform(-0.5, 0.3)   # 어깨 (Joint 2)
        j3 = random.uniform(-0.3, 0.5)   # 팔꿈치 (Joint 3)
        j4 = random.uniform(-0.5, 0.5)   # 손목 (Joint 4)
        
        point.positions = [j1, j2, j3, j4]
        point.time_from_start = Duration(sec=2, nanosec=0) # 2초 동안 이동
        
        msg.points.append(point)

        self.get_logger().info(f'🎲 목표 관절각: J1={j1:.2f}, J2={j2:.2f}, J3={j3:.2f}, J4={j4:.2f}')
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RandomManipulatorMove()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()