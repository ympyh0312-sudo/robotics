#!/bin/bash
# 컨테이너 진입점이자 ~/.bashrc 에서 source 되는 ROS 환경 설정 파일이다.
# ROS setup 스크립트가 미정의 변수를 참조하므로 set -e / set -u 를 쓰지 않는다.

source /opt/ros/jazzy/setup.bash

# /ros2_ws/install 은 ws_jazzy/install 로 겹쳐 마운트된 Jazzy 전용 경로다.
if [ -f /ros2_ws/install/setup.bash ]; then
  source /ros2_ws/install/setup.bash
fi

# Qt/Gazebo 가 요구하는 런타임 디렉터리.
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp/runtime-$(id -u)}"
mkdir -p "$XDG_RUNTIME_DIR"
chmod 0700 "$XDG_RUNTIME_DIR"

# source 된 경우(bashrc)에는 여기서 끝낸다. 실행된 경우에만 명령을 넘긴다.
(return 0 2>/dev/null) && return 0
exec "$@"
