#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    # ============================================================
    # PACKAGE DIRECTORY
    # ============================================================

    bringup_pkg = get_package_share_directory(
        'my_robot_bringup'
    )

    # ============================================================
    # SLAM TOOLBOX CONFIGURATION
    # ============================================================

    slam_params_file = os.path.join(
        bringup_pkg,
        'config',
        'slam_toolbox.yaml'
    )

    if not os.path.isfile(slam_params_file):
        raise FileNotFoundError(
            f'\nSLAM parameter file not found:\n'
            f'{slam_params_file}\n'
        )

    print(
        f'Using SLAM configuration:\n'
        f'{slam_params_file}'
    )

    # ============================================================
    # SLAM TOOLBOX
    # ============================================================

    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',

        name='slam_toolbox',

        output='screen',

        parameters=[
            slam_params_file,

            {
                'use_sim_time': True,
            }
        ]
    )

    # ============================================================
    # RETURN
    # ============================================================

    return LaunchDescription([

        slam_toolbox,

    ])