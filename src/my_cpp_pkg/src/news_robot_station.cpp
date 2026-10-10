#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class RobotNewsStation : public rclcpp::Node {
public:
    RobotNewsStation() : Node("robot_news_station") {
        pub_ = create_publisher<std_msgs::msg::String>("/robot_news", 10);
        timer_ = create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&RobotNewsStation::publishNews, this));
    }

private:
    void publishNews() {
        auto msg = std_msgs::msg::String();
        msg.data = "News from " + std::string(get_name());
        pub_->publish(msg);
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<RobotNewsStation>());
    rclcpp::shutdown();
}