import rclpy
from rclpy.node import Node
from my_robot_interface.srv import AddTwoInts
from functools import partial

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__("add_two_ints_clinet")
        self.call_add_two_ints(3,4)

    def call_add_two_ints(self, a, b):
        client = self.create_client(AddTwoInts, "add_two_ints")
        while not client.wait_for_service(timeout_sec = 1.0):
            self.get_logger().warning("Waiting for server...")

        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_call, a = a, b = b))

    def callback_call(self, future, a, b):
        response = future.result()
        self.get_logger().info(f"{a} + {b} = {response.sum}")

def main(args = None):
    rclpy.init(args = args)
    rclpy.spin(AddTwoIntsClient())
    rclpy.shutdown()