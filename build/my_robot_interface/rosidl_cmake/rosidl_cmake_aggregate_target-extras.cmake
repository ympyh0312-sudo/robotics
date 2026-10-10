# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target my_robot_interface::my_robot_interface
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${my_robot_interface_TARGETS}.
if(my_robot_interface_TARGETS AND NOT TARGET my_robot_interface::my_robot_interface)
  add_library(my_robot_interface::my_robot_interface INTERFACE IMPORTED)
  set_target_properties(my_robot_interface::my_robot_interface PROPERTIES
    INTERFACE_LINK_LIBRARIES "${my_robot_interface_TARGETS}")
endif()
