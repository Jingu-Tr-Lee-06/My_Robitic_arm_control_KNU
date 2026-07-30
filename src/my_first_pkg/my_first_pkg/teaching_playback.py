import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_srvs.srv import SetBool
from builtin_interfaces.msg import Duration
import sys, select, termios, tty, time

class TeachingPlayback(Node):
    def __init__(self):
        super().__init__('teaching_playback')
        
        # 현재 관절 상태 구독
        self.create_subscription(JointState, '/joint_states', self.joint_callback, 10)
        # 로봇 팔 및 그리퍼 퍼블리셔
        self.arm_pub = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        self.gripper_pub = self.create_publisher(JointTrajectory, '/gripper_controller/joint_trajectory', 10)
        # 토크 제어 서비스 클라이언트
        self.torque_client = self.create_client(SetBool, '/dynamixel_hardware_interface/set_dxl_torque')
        
        self.target_arm_joints = ['joint1', 'joint2', 'joint3', 'joint4']
        self.current_arm_joints = [0.0, 0.0, 0.0, 0.0]
        self.current_gripper_pos = 0.01  # 기본 열림 상태
        
        # 저장할 좌표 데이터 (팔 관절 4개, 그리퍼 위치)
        self.saved_waypoints = []
        self.has_joint_data = False
        
        print('\n' + '='*60)
        print('[모션 티칭 플레이백 노드]')
        print(' - [ t ] 키 : 팔 토크 OFF (손으로 팔을 자유롭게 이동)')
        print(' - [ g ] 키 : 집게 열기 (Gripper Open)')
        print(' - [ f ] 키 : 집게 닫기 (Gripper Close)')
        print(' - [Enter]  : 현재 위치 저장 (팔 각도 + 집게 상태 함께 기록)')
        print(' - [ p ] 키 : 토크 ON + 시작점으로 이동 후 매크로 재생')
        print(' - [ q ] 키 : 종료')
        print('='*60 + '\n')

    def joint_callback(self, msg):
        temp_arm = [None] * 4
        for i, name in enumerate(msg.name):
            if name in self.target_arm_joints:
                idx = self.target_arm_joints.index(name)
                if i < len(msg.position):
                    temp_arm[idx] = msg.position[i]
            elif name == 'gripper' and i < len(msg.position):
                self.current_gripper_pos = msg.position[i]

        if None not in temp_arm:
            self.current_arm_joints = temp_arm
            self.has_joint_data = True

    def set_torque_sync(self, enable: bool):
        if not self.torque_client.wait_for_service(timeout_sec=1.0):
            print("토크 서비스 연결 실패")
            return False
        
        req = SetBool.Request()
        req.data = enable
        future = self.torque_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result().success if future.result() else False

    def set_gripper(self, position: float):
        msg = JointTrajectory()
        msg.joint_names = ['gripper']
        point = JointTrajectoryPoint()
        point.positions = [position]
        point.time_from_start = Duration(sec=1, nanosec=0)
        msg.points.append(point)
        self.gripper_pub.publish(msg)
        self.current_gripper_pos = position

    def record_waypoint(self):
        if not self.has_joint_data:
            print("로봇 관절 데이터를 대기 중")
            return
            
        arm_pos = list(self.current_arm_joints)
        grp_pos = self.current_gripper_pos
        self.saved_waypoints.append((arm_pos, grp_pos))
        
        status_str = "열림" if grp_pos > 0 else "닫힘"
        print(f"[저장됨 #{len(self.saved_waypoints)}] 팔: {[round(x, 2) for x in arm_pos]} | 집게: {status_str}")

    def play_trajectory(self):
        if not self.saved_waypoints:
            print("저장된 좌표가 없음")
            return

        print("\n모터 토크 ON 설정 중")
        if self.set_torque_sync(True):
            print("토크 ON")
        
        time.sleep(0.5)

        # ---------------------------------------------------------------------
        # 핵심 개선: 현재 손 위치에서 1번 저장 위치까지 4초간 '천천히' 안전 이동
        # ---------------------------------------------------------------------
        start_arm_pos, start_grp_pos = self.saved_waypoints[0]
        print("1번 시작 위치로 이동")

        # 1번 위치 이동 명령 (팔)
        init_arm_msg = JointTrajectory()
        init_arm_msg.joint_names = self.target_arm_joints
        p_init_arm = JointTrajectoryPoint()
        p_init_arm.positions = start_arm_pos
        p_init_arm.time_from_start = Duration(sec=4, nanosec=0)
        init_arm_msg.points.append(p_init_arm)
        self.arm_pub.publish(init_arm_msg)

        # 1번 위치 이동 명령 (그리퍼)
        init_grp_msg = JointTrajectory()
        init_grp_msg.joint_names = ['gripper']
        p_init_grp = JointTrajectoryPoint()
        p_init_grp.positions = [start_grp_pos]
        p_init_grp.time_from_start = Duration(sec=4, nanosec=0)
        init_grp_msg.points.append(p_init_grp)
        self.gripper_pub.publish(init_grp_msg)

        # 시작 위치 도착 시까지 대기
        time.sleep(4.2)

        # ---------------------------------------------------------------------
        # 3. 시작 위치 정착 후 저장된 매크로 동작 순차 재생 (각 포인트간 3.0초)
        # ---------------------------------------------------------------------
        print(f"저장된 {len(self.saved_waypoints)}개 매크로 동작 재생")
        
        step_time = 2.0  # 경유지 간 이동 시간 (초)
        for i, (arm_pos, grp_pos) in enumerate(self.saved_waypoints):
            exec_sec = int(step_time * (i + 1))
            exec_nano = int((step_time * (i + 1) % 1) * 1e9)
            
            # 팔 동작
            arm_msg = JointTrajectory()
            arm_msg.joint_names = self.target_arm_joints
            p_arm = JointTrajectoryPoint()
            p_arm.positions = arm_pos
            p_arm.time_from_start = Duration(sec=exec_sec, nanosec=exec_nano)
            arm_msg.points.append(p_arm)
            self.arm_pub.publish(arm_msg)

            # 집게 동작
            grp_msg = JointTrajectory()
            grp_msg.joint_names = ['gripper']
            p_grp = JointTrajectoryPoint()
            p_grp.positions = [grp_pos]
            p_grp.time_from_start = Duration(sec=exec_sec, nanosec=exec_nano)
            grp_msg.points.append(p_grp)
            self.gripper_pub.publish(grp_msg)
            
        print("매크로 동작 실행 중\n")

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1) if rlist else ''
    termios.tcsetattr(sys.stdin, sys.stdin.fileno(), settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = TeachingPlayback()
    
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            key = get_key(settings)
            
            if key == 't':  # 토크 OFF
                if node.set_torque_sync(False):
                    print("\n팔 토크 해제, 수동 조작 모드")
            elif key == 'g':  # 집게 열기
                print("집게 열기")
                node.set_gripper(0.01)
            elif key == 'f':  # 집게 닫기
                print("집게 닫기")
                node.set_gripper(-0.01)
            elif key == '\r' or key == '\n':  # Enter (저장)
                node.record_waypoint()
            elif key == 'p':  # 재생
                node.play_trajectory()
            elif key == 'q':  # 종료
                break
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()