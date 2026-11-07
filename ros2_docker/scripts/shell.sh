#!/usr/bin/env bash
# 실행 중인 컨테이너에 접속한다. 터미널을 여러 개 열어도 된다.
# 인자를 주면 그 명령만 ROS 환경에서 실행한다. 예: ./scripts/shell.sh ros2 topic list
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
require_compose

if [ "$(docker inspect -f '{{.State.Running}}' ros2_jazzy 2>/dev/null)" != "true" ]; then
  echo "오류: 컨테이너가 실행 중이 아닙니다. 먼저 ./scripts/start.sh 를 실행하세요." >&2
  exit 1
fi

tty_flag=()
[ -t 0 ] && [ -t 1 ] || tty_flag=(-T)

if [ "$#" -eq 0 ]; then
  exec docker compose exec ros2 bash
fi
exec docker compose exec "${tty_flag[@]}" ros2 /ros_entrypoint.sh "$@"
