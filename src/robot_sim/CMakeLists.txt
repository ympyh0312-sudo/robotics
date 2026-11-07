cmake_minimum_required(VERSION 3.20)
project(robot_sim)

find_package(ament_cmake REQUIRED)

# 데이터 파일을 install/share/robot_sim/ 으로 복사한다.
# ros2 launch 와 FindPackageShare 는 이 위치에서 파일을 찾는다.
install(DIRECTORY worlds models launch config rviz maps
  DESTINATION share/${PROJECT_NAME})

# map_publisher 노드와 그것이 쓰는 모듈. 같은 폴더에 있어야 import 가 된다.
install(PROGRAMS scripts/map_publisher.py DESTINATION lib/${PROJECT_NAME})
install(FILES scripts/grid_map.py DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
