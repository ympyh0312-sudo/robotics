#!/usr/bin/env bash
# 호스트에 Docker Compose/Buildx 를, 선택적으로 NVIDIA 컨테이너 런타임을 설치한다.
# 사용법: sudo ./scripts/install-host-deps.sh [--nvidia]
#
# docker-compose-v2, docker-buildx : Ubuntu 26.04 공식 저장소 패키지 (설치된 docker.io 와 같은 계열)
# nvidia-container-toolkit         : NVIDIA 공식 저장소 패키지
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "오류: sudo 로 실행하세요." >&2
  exit 1
fi

apt-get update
apt-get install -y docker-compose-v2 docker-buildx

if [ "${1:-}" = "--nvidia" ]; then
  apt-get install -y curl gnupg
  curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
  curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    -o /etc/apt/sources.list.d/nvidia-container-toolkit.list
  apt-get update
  apt-get install -y nvidia-container-toolkit

  # /etc/docker/daemon.json 에 nvidia 런타임을 등록한다. 재시작 중 실행 중인 컨테이너는 멈춘다.
  nvidia-ctk runtime configure --runtime=docker
  systemctl restart docker
fi

docker compose version
docker buildx version
