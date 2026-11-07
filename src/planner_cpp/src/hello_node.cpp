#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class HelloNode : public rclcpp::Node
{
public:
  HelloNode()
  : Node("planner_cpp_hello")
  {
    timer_ = create_wall_timer(1s, [this]() {
          RCLCPP_INFO(get_logger(), "planner_cpp alive: %d", ++count_);
        });
  }

private:
  rclcpp::TimerBase::SharedPtr timer_;
  int count_{0};
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<HelloNode>());
  rclcpp::shutdown();
  return 0;
}
