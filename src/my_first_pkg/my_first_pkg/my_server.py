import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MyServer(Node):
    def __init__(self):
        super().__init__('my_server_node')
        # 'add_two_ints'라는 이름의 서비스 서버 생성 (입력받은 두 정수를 더해주는 기본 제공 인터페이스 사용)
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('My Service Server has been started.')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}')
        self.get_logger().info(f'Sending response: sum={response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = MyServer()
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