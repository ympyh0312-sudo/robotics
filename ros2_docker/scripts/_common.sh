#!/usr/bin/env bash
# 다른 스크립트에서 source 하는 공통 설정.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

[ -f .env ] || cp .env.example .env
set -a
source ./.env
set +a

export HOST_UID="$(id -u)"
export HOST_GID="$(id -g)"
export RENDER_GID="$(getent group render | cut -d: -f3 || true)"
export VIDEO_GID="$(getent group video | cut -d: -f3 || true)"
export DISPLAY="${DISPLAY:-:0}"

require_compose() {
  if ! docker compose version >/dev/null 2>&1; then
    echo "오류: docker compose 플러그인이 없습니다." >&2
    echo "설치: sudo ./scripts/install-host-deps.sh" >&2
    exit 1
  fi
}

resolve_gpu_mode() {
  local mode="${GPU_MODE:-auto}"
  if [ "$mode" = "auto" ]; then
    if docker info --format '{{range $k, $v := .Runtimes}}{{$k}} {{end}}' 2>/dev/null | grep -qw nvidia \
        && nvidia-smi >/dev/null 2>&1; then
      mode=nvidia
    elif compgen -G '/dev/dri/renderD*' >/dev/null; then
      mode=dri
    else
      mode=cpu
    fi
  fi
  case "$mode" in
    nvidia|dri|cpu) echo "$mode" ;;
    *) echo "오류: 알 수 없는 GPU_MODE: $mode (auto|nvidia|dri|cpu)" >&2; exit 1 ;;
  esac
}

compose() {
  docker compose -f docker-compose.yml -f "docker-compose.$(resolve_gpu_mode).yml" "$@"
}
