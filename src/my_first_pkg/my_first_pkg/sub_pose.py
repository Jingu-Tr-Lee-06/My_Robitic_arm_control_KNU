import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class SubPose(Node):
    def __init__(self):
        super().__init__('sub_pose_node')
        # /turtle1/pose 토픽을 구독하는 Subscriber 생성
        # 메시지 타입: turtlesim.msg.Pose
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        self.subscription  # warning 방지용

    def pose_callback(self, msg):
        # x, y 좌표 및 theta(방향각) 수신 로그 출력
        self.get_logger().info(f'Turtle Pose -> X: {msg.x:.2f}, Y: {msg.y:.2f}, Theta: {msg.theta:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = SubPose()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()