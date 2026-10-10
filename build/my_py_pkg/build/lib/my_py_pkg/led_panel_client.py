# LED 3개(켜짐/꺼짐) 목록을 관리하는 `led_panel` 서비스 서버를 만드세요. `int64 led_number`와 `bool state`를 받는 `SetLed` 서비스 호출을 받아 `bool success`와 `string message`를 반환합니다.
# CLIENT

import rclpy
from rclpy.node import Node
from my_robot_interface.srv import SetLed
from functools import partial

class LedPanelClient(Node):
    def __init__(self):
        super().__init__('led_panel_client')
        self.call_led_panel(0, True)
        self.call_led_panel(1, False)
        self.call_led_panel(2, True)
        self.call_led_panel(3, True)  # Invalid LED number

    def call_led_panel(self, led_number, state):
        client = self.create_client(SetLed, 'led_panel')
        while not client.wait_for_service(timeout_sec = 1.0):
            self.get_logger().warning('Waiting for server...')

        request = SetLed.Request()
        request.led_number = led_number
        request.state = state
        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_call, led_number = led_number, state = state))

    def callback_call(self, future, led_number, state):
        response = future.result()
        if response.success:
            self.get_logger().info(f"LED {led_number} set to {'ON' if state else 'OFF'}: {response.message}")
        else:
            self.get_logger().error(f"Failed to set LED {led_number}: {response.message}")

def main(args = None):
    rclpy.init(args = args)
    rclpy.spin(LedPanelClient())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
