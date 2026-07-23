import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MyClient(Node):
    def __init__(self):
        super().__init__('my_client_node')
        # 'add_two_ints' 서비스 클라이언트 생성
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        
        # 서버가 켜질 때까지 대기
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        # 비동기로 요청을 보내고 응답을 기다림
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    node = MyClient()
    
    # 실행 시 전달된 인자가 있으면 사용, 없으면 기본값(교통정리용 기본 숫자 2, 3) 사용
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    node.get_logger().info(f'Requesting: {a} + {b}')
    response = node.send_request(a, b)
    node.get_logger().info(f'Received response: sum = {response.sum}')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()