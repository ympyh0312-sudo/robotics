#!/usr/bin/env bash
# 컨테이너를 정지한다. 컨테이너와 이미지, 빌드 결과는 삭제하지 않는다.
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
require_compose

compose stop
echo "정지됨: ros2_jazzy (다시 시작: ./scripts/start.sh)"
