#!/usr/bin/env bash
# 개발 이미지를 빌드한다. 추가 인자는 docker compose build 로 전달된다 (예: --no-cache).
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
require_compose

compose build "$@"
echo "빌드 완료: ${IMAGE_NAME:-ros2-jazzy-dev:latest}"
