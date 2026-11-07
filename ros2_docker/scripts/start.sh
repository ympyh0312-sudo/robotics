#!/usr/bin/env bash
# 컨테이너를 백그라운드로 시작하고 GUI 접근을 허용한다.
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
require_compose

# 겹쳐 마운트할 경로를 현재 사용자 소유로 미리 만든다.
ws_path="${ROS2_WS:-$HOME/ros2_ws}"
mkdir -p ws_jazzy/build ws_jazzy/install ws_jazzy/log \
         "$ws_path/build" "$ws_path/install" "$ws_path/log"

# 같은 UID 의 로컬 프로세스만 X 서버에 허용한다. (xhost + 처럼 전체를 열지 않는다.)
if command -v xhost >/dev/null 2>&1 && [ -S "/tmp/.X11-unix/X${DISPLAY#*:}" ]; then
  xhost "+SI:localuser:$(id -un)" >/dev/null \
    || echo "경고: xhost 설정 실패. GUI 가 열리지 않을 수 있습니다." >&2
else
  echo "경고: X 소켓을 찾지 못했습니다 (DISPLAY=$DISPLAY). headless 로만 사용할 수 있습니다." >&2
fi

gpu_mode="$(resolve_gpu_mode)"
compose up -d
echo "시작됨: ros2_jazzy (GPU_MODE=$gpu_mode, ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-30}, 세션=${XDG_SESSION_TYPE:-unknown})"
echo "접속: ./scripts/shell.sh"
