import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoveTurtle(Node):
    def __init__(self):
        super().__init__('move_turtle_node')
        # /turtle1/cmd_vel 토픽으로 Twist 메시지를 발행하는 Publisher 생성
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 0.1초(10Hz)마다 timer_callback 함수 호출
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 2.0   # 전진 속도
        msg.angular.z = 1.0  # 회전 속도 (원을 그리며 이동)
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: linear.x=2.0, angular.z=1.0')

def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()