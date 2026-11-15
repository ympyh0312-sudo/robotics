ARG BASE_IMAGE=osrf/ros:jazzy-desktop
FROM ${BASE_IMAGE}

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG ROS_USER=ros

ENV ROS_DISTRO=jazzy \
    GZ_VERSION=harmonic \
    ROS_WS=/ros2_ws \
    DEBIAN_FRONTEND=noninteractive

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

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ros-jazzy-slam-toolbox \
      ros-jazzy-nav2-map-server \
      ros-jazzy-teleop-twist-keyboard \
 && apt-get clean

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

COPY ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod 0755 /ros_entrypoint.sh

USER ${HOST_UID}
RUN echo 'source /ros_entrypoint.sh' >> "${HOME:-/home/ros}/.bashrc" \
 && rosdep update --rosdistro "${ROS_DISTRO}"

WORKDIR ${ROS_WS}
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]