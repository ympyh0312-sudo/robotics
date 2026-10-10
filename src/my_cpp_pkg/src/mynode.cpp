#include "rclcpp/rclcpp.hpp"

class MyNode : public rclcpp::Node {
public:
    MyNode() : Node("my_node") {
        declare_parameter("robot_name", "my_robot");
        declare_parameter("move_speed", 1.5);
        auto name = get_parameter("robot_name").as_string();
        auto speed = get_parameter("move_speed").as_double();
        RCLCPP_INFO(get_logger(), "Robot: %s, Speed: %.2f", name.c_str(), speed);
    }
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
