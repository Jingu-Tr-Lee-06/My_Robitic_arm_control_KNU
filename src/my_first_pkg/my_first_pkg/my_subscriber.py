import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MySubscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber_node')
        # '/my_message' 토픽을 구독하고, 데이터가 들어오면 listener_callback 함수 실행
        self.subscription = self.create_subscription(
            String,
            '/my_message',
            self.listener_callback,
            10
        )
        self.get_logger().info('My Subscriber Node has been started.')

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()