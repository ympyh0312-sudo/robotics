#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class SmartphoneNode : public rclcpp::Node {
public:
    SmartphoneNode() : Node("smartphone") {
        sub_ = create_subscription<std_msgs::msg::String>(
            "/robot_news", 10,
            std::bind(&SmartphoneNode::callbackRobotNews, this,
                      std::placeholders::_1));
    }

private:
    void callbackRobotNews(const std_msgs::msg::String::SharedPtr msg) {
        RCLCPP_INFO(get_logger(), "Received: %s", msg->data.c_str());
    }

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SmartphoneNode>());
    rclcpp::shutdown();
    return 0;
}