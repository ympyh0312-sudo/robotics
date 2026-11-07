# ROS 2 Jazzy + Gazebo Harmonic + RViz2 개발 이미지 (Ubuntu 24.04)
# 빌드는 ./scripts/build.sh 를 사용한다. 인자는 .env / docker-compose.yml 에서 전달된다.
ARG BASE_IMAGE=osrf/ros:jazzy-desktop
FROM ${BASE_IMAGE}

# 컨테이너 사용자를 호스트 UID/GID와 맞춘다. 마운트한 ~/ros2_ws 의 파일 소유권이
# 어긋나지 않고, X11 접근도 xhost +SI:localuser 로 허용할 수 있다.
ARG HOST_UID=1000
ARG HOST_GID=1000
ARG ROS_USER=ros

ENV ROS_DISTRO=jazzy \
    GZ_VERSION=harmonic \
    ROS_WS=/ros2_ws \
    DEBIAN_FRONTEND=noninteractive

# 개발 도구, Gazebo Harmonic(ros-jazzy-ros-gz 가 Harmonic vendor 패키지를 포함),
# ROS-Gazebo bridge, GUI/GPU 사용자 공간 라이브러리, 장치 진단 도구를 설치한다.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ros-dev-tools \
      python3-colcon-common-extensions \
      python3-rosdep \
      build-essential \
      git \
      ros-jazzy-rviz2 \
      ros-jazzy-demo-nodes-cpp \
      ros-jazzy-demo-nodes-py \
      ros-jazzy-ros-gz \
      ros-jazzy-ros-gz-sim \
      ros-jazzy-ros-gz-bridge \
      ros-jazzy-ros-gz-image \
      ros-jazzy-ros-gz-sim-demos \
      mesa-utils \
      libgl1-mesa-dri \
      libglx-mesa0 \
      libegl-mesa0 \
      libgbm1 \
      libglvnd0 \
      libegl1 \
      libvulkan1 \
      mesa-vulkan-drivers \
      vulkan-tools \
      x11-apps \
      x11-utils \
      x11-xserver-utils \
      v4l-utils \
      usbutils \
      iputils-ping \
      bash-completion \
      less \
      nano \
      sudo \
 && apt-get clean

# 호스트 UID/GID 를 가진 개발 사용자. 베이스 이미지에 같은 UID 사용자(ubuntu)가 있으면 재사용한다.
# 장치 접근 그룹(video, dialout, plugdev)을 미리 부여한다.
RUN if ! getent group "${HOST_GID}" >/dev/null; then groupadd -g "${HOST_GID}" "${ROS_USER}"; fi \
 && if ! getent passwd "${HOST_UID}" >/dev/null; then \
      useradd -m -s /bin/bash -u "${HOST_UID}" -g "${HOST_GID}" "${ROS_USER}"; \
    fi \
 && dev_user="$(getent passwd "${HOST_UID}" | cut -d: -f1)" \
 && usermod -g "${HOST_GID}" -s /bin/bash -aG video,dialout,plugdev,sudo "${dev_user}" \
 && echo "${dev_user} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ros-dev \
 && chmod 0440 /etc/sudoers.d/ros-dev \
 && mkdir -p "${ROS_WS}" \
 && chown "${HOST_UID}:${HOST_GID}" "${ROS_WS}"

# 베이스 이미지의 /ros_entrypoint.sh 를 교체한다.
COPY ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod 0755 /ros_entrypoint.sh

# GID 를 함께 지정하면 보조 그룹(dialout 등)이 적용되지 않으므로 UID 만 지정한다.
USER ${HOST_UID}
# 대화형 bash 에서 ROS 환경을 자동으로 불러온다.
RUN echo 'source /ros_entrypoint.sh' >> "${HOME:-/home/ros}/.bashrc" \
 && rosdep update --rosdistro "${ROS_DISTRO}"

WORKDIR ${ROS_WS}
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
