#!/usr/bin/env bash
# GUI 없이 Gazebo 와 ROS-Gazebo bridge 를 검증한다. 현재 GPU_MODE 로 실행 중인 컨테이너를 사용한다.
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

docker exec -i ros2_jazzy /ros_entrypoint.sh bash -s <<'EOF'
world=/opt/ros/jazzy/opt/gz_sim_vendor/share/gz/gz-sim8/worlds/visualize_lidar.sdf
cmd_vel=/model/vehicle_blue/cmd_vel
fail=0
report() { if [ "$2" -eq 0 ]; then echo "[PASS] $1"; else echo "[FAIL] $1"; fail=1; fi; }

timeout 45 gz sim -s -r --headless-rendering -v 2 "$world" >/tmp/gz_server.log 2>&1 &
timeout 40 ros2 run ros_gz_bridge parameter_bridge \
  '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock' \
  '/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan' \
  "${cmd_vel}@geometry_msgs/msg/Twist]gz.msgs.Twist" >/tmp/gz_bridge.log 2>&1 &
sleep 8

gz_stats="$(timeout 8 gz topic -e -n 1 -t /stats 2>/dev/null)"
[ -n "$gz_stats" ]; report "Gazebo 서버 시뮬레이션 진행 (/stats)" $?
echo "$gz_stats" | grep -E '^(real_time_factor|paused)' | sed 's/^/       /'

timeout 8 ros2 topic echo --once /clock >/tmp/clock.out 2>&1
report "bridge Gazebo -> ROS (/clock)" $?

timeout 12 ros2 topic echo --once --field ranges /lidar >/tmp/lidar.out 2>&1
report "bridge Gazebo -> ROS, 렌더링 센서 (/lidar)" $?

timeout 12 gz topic -e -n 1 -t "$cmd_vel" >/tmp/cmd_vel.out 2>&1 &
sleep 1
ros2 topic pub --times 6 --rate 2 "$cmd_vel" geometry_msgs/msg/Twist '{linear: {x: 0.5}}' >/dev/null 2>&1
grep -q 'x: 0.5' /tmp/cmd_vel.out
report "bridge ROS -> Gazebo (cmd_vel)" $?

grep -iE 'error|failed|egl' /tmp/gz_server.log | sort -u | head -5 | sed 's/^/       log: /'
wait
exit "$fail"
EOF
