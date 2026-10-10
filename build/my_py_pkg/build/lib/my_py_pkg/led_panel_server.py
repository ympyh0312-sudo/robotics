# LED 3개(켜짐/꺼짐) 목록을 관리하는 `led_panel` 서비스 서버를 만드세요. `int64 led_number`와 `bool state`를 받는 `SetLed` 서비스 호출을 받아 `bool success`와 `string message`를 반환합니다.
# SERVER
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_robot_interface.srv import SetLed

class LedPanelServer(Node):
    def __init__(self):
        super().__init__('led_panel_server')
        self.server_ = self.create_service(SetLed, 'led_panel', self.callback_led_panel)
        self.led_states = [False, False, False]
        self.get_logger().info("LED Panel server started")

    def callback_led_panel(self, request, response):
        led_number = request.led_number
        state = request.state

        if 0 <= led_number < len(self.led_states):
            self.led_states[led_number] = state
            response.success = True
            response.message = f"LED {led_number} set to {'ON' if state else 'OFF'}"
            self.get_logger().info(response.message)
            return response
        else:
            response.success = False
            response.message = f"Invalid LED number: {led_number}"
            self.get_logger().warning(response.message)
            return response

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(LedPanelServer())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
