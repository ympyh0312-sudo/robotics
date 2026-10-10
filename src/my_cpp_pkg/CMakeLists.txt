cmake_minimum_required(VERSION 3.20)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(my_robot_interface REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

add_executable(my_first_node src/my_first_node.cpp)
target_link_libraries(my_first_node PUBLIC rclcpp::rclcpp)
install(TARGETS my_first_node DESTINATION lib/${PROJECT_NAME})

add_executable(news_robot_station src/news_robot_station.cpp)
target_link_libraries(news_robot_station PUBLIC rclcpp::rclcpp ${std_msgs_TARGETS})

add_executable(smartphonenode src/smartphonenode.cpp)
target_link_libraries(smartphonenode PUBLIC rclcpp::rclcpp ${std_msgs_TARGETS})

add_executable(addtwointserver src/addtwointserver.cpp)
target_link_libraries(addtwointserver PUBLIC rclcpp::rclcpp ${my_robot_interface_TARGETS})
install(TARGETS addtwointserver DESTINATION lib/${PROJECT_NAME})

add_executable(mynode src/mynode.cpp)
target_link_libraries(mynode PUBLIC rclcpp::rclcpp)
install(TARGETS mynode DESTINATION lib/${PROJECT_NAME})

install(TARGETS
  news_robot_station
  smartphonenode
  DESTINATION lib/${PROJECT_NAME})

ament_package()