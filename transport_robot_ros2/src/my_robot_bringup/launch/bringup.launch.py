from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    bringup_pkg = get_package_share_directory('my_robot_bringup')

    # =========================================================
    # 1. GAZEBO
    # =========================================================

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                bringup_pkg,
                'launch',
                'gazebo.launch.py'
            )
        )
    )

    # =========================================================
    # 2. JOINT STATE BROADCASTER
    # =========================================================

    joint_state_broadcaster = TimerAction(
        period=5.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2',
                    'run',
                    'controller_manager',
                    'spawner',
                    'joint_state_broadcaster',
                    '--controller-manager',
                    '/controller_manager'
                ],
                output='screen'
            )
        ]
    )

    # =========================================================
    # 3. OMNI DRIVE CONTROLLER
    # =========================================================

    omni_drive_controller = TimerAction(
        period=7.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2',
                    'run',
                    'controller_manager',
                    'spawner',
                    'omni_drive_controller',
                    '--controller-manager',
                    '/controller_manager'
                ],
                output='screen'
            )
        ]
    )

    # =========================================================
    # 4. RVIZ
    # =========================================================

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                bringup_pkg,
                'launch',
                'rviz.launch.py'
            )
        )
    )

    # =========================================================
    # 5. SLAM TOOLBOX
    # =========================================================

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                bringup_pkg,
                'launch',
                'slam.launch.py'
            )
        )
    )

    # =========================================================
    # 6. KEYBOARD / PYGAME TELEOP
    # =========================================================

    teleop_script = os.path.join(
        bringup_pkg,
        'scripts',
        'keyboard_teleop.py'
    )

    teleop = TimerAction(
        period=9.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'python3',
                    teleop_script
                ],
                output='screen'
            )
        ]
    )

    # =========================================================
    # RETURN ALL NODES / PROCESSES
    # =========================================================

    return LaunchDescription([
        # Start Gazebo first
        gazebo_launch,

        # Then controllers
        joint_state_broadcaster,
        omni_drive_controller,

        # Visualization
        rviz_launch,

        # SLAM
        slam_launch,

        # Teleop
        teleop,
    ])
