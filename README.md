# 🚚 Transport Robot ROS 2 — Gazebo Simulation

A ROS 2 Jazzy simulation of a custom **omnidirectional transport robot** running in Gazebo Sim.

The project includes:

* 🤖 Custom transport robot model
* 🛞 Four-wheel omni-drive system
* 🎮 Keyboard teleoperation
* 🌎 Custom Gazebo simulation world
* 📡 LiDAR
* 📷 RGB camera
* 🧭 SLAM Toolbox
* 🗺️ 2D mapping
* 👁️ RViz visualization
* 🔄 ROS 2 ↔ Gazebo communication
* ⚙️ ros2_control-based wheel control

The project is designed so that the complete simulation can be cloned and built from a clean Ubuntu 24.04 + ROS 2 Jazzy installation.

---

## 📸 Simulation

> Add screenshots/GIFs of the robot, Gazebo and RViz here.

Example:

```text
docs/images/gazebo.png
docs/images/rviz.png
docs/images/slam.png
```

---

# 🧰 Requirements

## Operating System

* Ubuntu 24.04 LTS

## ROS 2

* ROS 2 Jazzy Jalisco

## Simulation

* Gazebo Sim
* `ros_gz`
* `ros_gz_sim`
* `ros_gz_bridge`

## Other ROS 2 packages

The project also uses:

* `xacro`
* `robot_state_publisher`
* `joint_state_publisher_gui`
* `rviz2`
* `slam_toolbox`
* `ros2_control`
* `controller_manager`

---

# 📦 Installation

## 1. Install ROS 2 Jazzy

Follow the official ROS 2 Jazzy installation instructions for Ubuntu 24.04.

After installing ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

---

## 2. Install required ROS packages

```bash
sudo apt update
```

```bash
sudo apt install -y \
    ros-jazzy-xacro \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-rviz2 \
    ros-jazzy-slam-toolbox \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers
```

---

# 📥 Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/transport_robot_ros2.git
```

Enter the repository:

```bash
cd transport_robot_ros2
```

---

# 🏗️ Build

Source ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Build the workspace:

```bash
colcon build --symlink-install
```

Source the workspace:

```bash
source install/setup.bash
```

---

# 🚀 Start the Simulation

The easiest way to start the project is:

```bash
ros2 launch my_robot_bringup bringup.launch.py
```

This launches the main simulation stack.

Depending on the current configuration, this includes:

* Gazebo
* Transport robot
* ROS ↔ Gazebo bridge
* Controllers
* RViz
* SLAM Toolbox

---

# 🎮 Keyboard Control

The robot can be controlled using the keyboard teleoperation node.

Run:

```bash
ros2 run my_robot_bringup keyboard_teleop.py
```

Or, if the script is launched through the main bringup system, use the configured teleoperation interface.

## Controls

| Key      | Action                   |
| -------- | ------------------------ |
| `W`      | Forward                  |
| `S`      | Backward                 |
| `A`      | Strafe left              |
| `D`      | Strafe right             |
| `Q`      | Rotate counter-clockwise |
| `E`      | Rotate clockwise         |
| `X`      | Stop                     |
| `CTRL+C` | Exit                     |

> Controls may be adjusted in `keyboard_teleop.py`.

The robot uses an omni-drive configuration, allowing translational and rotational motion.

---

# 🛞 Omni Drive

The robot uses four omni wheels.

The wheel configuration is:

```text
             FRONT
       ┌───────────────┐
       │               │
       │   ◉       ◉   │
       │               │
       │   ◉       ◉   │
       │               │
       └───────────────┘
              REAR
```

The wheel controller is configured through:

```text
src/my_robot_bringup/config/controllers.yaml
```

The controller accepts velocity commands on:

```text
/omni_drive_controller/cmd_vel
```

with:

```text
geometry_msgs/msg/TwistStamped
```

---

# 📡 Sensors

The robot contains several simulated sensors.

## LiDAR

ROS topic:

```text
/scan
```

Message type:

```text
sensor_msgs/msg/LaserScan
```

Check:

```bash
ros2 topic echo /scan
```

---

## RGB Camera

Image topic:

```text
/camera/image_raw
```

Camera information:

```text
/camera/camera_info
```

Check:

```bash
ros2 topic list | grep camera
```

---

# 🗺️ SLAM

The project uses **SLAM Toolbox** for 2D mapping.

Start SLAM separately if required:

```bash
ros2 launch my_robot_bringup slam.launch.py
```

SLAM consumes:

```text
/scan
```

and produces:

```text
/map
```

Check:

```bash
ros2 topic list | grep -E 'map|scan'
```

Expected topics include:

```text
/map
/scan
```

---

# 👁️ RViz

Start RViz:

```bash
ros2 launch my_robot_bringup rviz.launch.py
```

The RViz configuration is stored at:

```text
src/my_robot_bringup/rviz/display.rviz
```

RViz can be used to visualize:

* Robot model
* TF
* LiDAR scan
* Map
* Camera data
* Odometry
* Robot frames

---

# 🌎 Gazebo World

The simulation world is included inside the repository:

```text
src/my_robot_bringup/worlds/transport_world.sdf
```

The world is installed automatically with the ROS package.

The project does **not** require the original external:

```text
~/sdf_test/
```

directory.

The Gazebo launch file obtains the world using the installed ROS package path.

---

# 📁 Project Structure

```text
transport_robot_ros2/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── docs/
│   └── images/
│
└── src/
    │
    ├── my_robot_description/
    │   ├── package.xml
    │   ├── CMakeLists.txt
    │   │
    │   └── urdf/
    │       ├── transport_robot.xacro
    │       └── meshes/
    │           ├── base_link.stl
    │           ├── link1.stl
    │           ├── ...
    │           └── link16.stl
    │
    └── my_robot_bringup/
        ├── package.xml
        ├── CMakeLists.txt
        │
        ├── launch/
        │   ├── bringup.launch.py
        │   ├── gazebo.launch.py
        │   ├── rviz.launch.py
        │   └── slam.launch.py
        │
        ├── config/
        │   ├── controllers.yaml
        │   ├── slam_toolbox.yaml
        │   └── tr_gazebo_bridge.yaml
        │
        ├── rviz/
        │   └── display.rviz
        │
        ├── scripts/
        │   └── keyboard_teleop.py
        │
        └── worlds/
            └── transport_world.sdf
```

---

# 🔧 Useful Commands

## Check ROS packages

```bash
ros2 pkg list | grep my_robot
```

## Check robot description

```bash
ros2 topic echo /robot_description
```

## Check LiDAR

```bash
ros2 topic list | grep scan
```

```bash
ros2 topic info /scan
```

## Check camera

```bash
ros2 topic list | grep camera
```

## Check controllers

```bash
ros2 control list_controllers
```

## Check TF

```bash
ros2 run tf2_tools view_frames
```

## Check odometry

```bash
ros2 topic list | grep odom
```

---

# 🧹 Clean Build

If you encounter build or installation problems:

```bash
cd transport_robot_ros2
```

```bash
rm -rf build install log
```

Then:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

---

# 🐛 Troubleshooting

## Gazebo world not found

Make sure:

```text
src/my_robot_bringup/worlds/transport_world.sdf
```

exists.

Then rebuild:

```bash
rm -rf build install log
colcon build --symlink-install
source install/setup.bash
```

Check:

```bash
ls $(ros2 pkg prefix my_robot_bringup)/share/my_robot_bringup/worlds/
```

---

## Robot mesh not visible

Check that the meshes exist:

```bash
ls src/my_robot_description/urdf/meshes/
```

Make sure the Xacro uses:

```text
package://my_robot_description/urdf/meshes/
```

rather than an absolute filesystem path.

---

## `/scan` exists but `/map` does not

Check SLAM Toolbox:

```bash
ros2 node list | grep slam
```

Check:

```bash
ros2 topic list | grep -E 'map|scan|odom'
```

SLAM requires a valid TF chain between the laser, robot base and odometry frames.

---

# 🤝 Contributing

Contributions are welcome.

You can:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the simulation.
5. Open a pull request.

Example:

```bash
git checkout -b feature/my-new-feature
```

---

# 📜 License

This project is released under the MIT License.

See:

```text
LICENSE
```

for details.

---

# ⭐ Project Goals

The long-term goal of this project is to develop a complete simulated transport robot platform for:

* Robotics research
* ROS 2 learning
* Gazebo simulation
* Autonomous navigation
* SLAM
* Omni-directional movement
* Sensor integration
* Robot control
* RoboCON-style environments

---

# 🚀 Future Features

Planned improvements include:

* [ ] Improved omni-wheel friction model
* [ ] Complete odometry
* [ ] Reliable `odom → base_footprint` TF
* [ ] Improved SLAM configuration
* [ ] Autonomous navigation
* [ ] Nav2 integration
* [ ] Better camera visualization
* [ ] Gamepad/Bluetooth control
* [ ] Autonomous transport missions
* [ ] Dynamic obstacles
* [ ] Robot task/game logic
* [ ] Additional sensors
* [ ] Docker-based setup

---

## Author

**Ros_the_boss**

Built with:

* ROS 2 Jazzy
* Gazebo Sim
* Python
* C++
* ros2_control
* SLAM Toolbox
* RViz2

If you find this project useful, consider giving the repository a ⭐.
