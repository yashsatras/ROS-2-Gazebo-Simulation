#!/usr/bin/env python3

import os

import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    # ============================================================
    # PACKAGE DIRECTORIES
    # ============================================================

    robot_description_pkg = get_package_share_directory(
        'my_robot_description'
    )

    bringup_pkg = get_package_share_directory(
        'my_robot_bringup'
    )

    # ============================================================
    # XACRO FILE
    # ============================================================

    xacro_file = os.path.join(
        robot_description_pkg,
        'urdf',
        'transport_robot.xacro'
    )

    if not os.path.isfile(xacro_file):
        raise FileNotFoundError(
            f'\nXacro file not found:\n{xacro_file}\n'
        )

    print(f'Using Xacro:\n{xacro_file}')

    # ============================================================
    # PROCESS XACRO
    # ============================================================

    try:

        robot_description = xacro.process_file(
            xacro_file
        ).toxml()

    except Exception as e:

        raise RuntimeError(
            f'\nFailed to process Xacro:\n'
            f'{xacro_file}\n\n'
            f'Xacro error:\n{e}\n'
        )

    # ============================================================
    # RVIZ CONFIGURATION
    # ============================================================

    rviz_config = os.path.join(
        bringup_pkg,
        'rviz',
        'display.rviz'
    )

    if not os.path.isfile(rviz_config):
        raise FileNotFoundError(
            f'\nRViz configuration not found:\n'
            f'{rviz_config}\n'
        )

    # ============================================================
    # ROBOT STATE PUBLISHER
    # ============================================================

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',

        name='robot_state_publisher',

        output='screen',

        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True,
            }
        ]
    )

    # ============================================================
    # JOINT STATE PUBLISHER GUI
    # ============================================================
    #
    # This is useful when RViz is running WITHOUT Gazebo.
    #
    # When Gazebo + ros2_control is running, actual joint states
    # should come from the controllers instead.
    #
    # ============================================================

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',

        name='joint_state_publisher_gui',

        output='screen',

        parameters=[
            {
                'use_sim_time': True,
            }
        ]
    )

    # ============================================================
    # RVIZ2
    # ============================================================

    rviz = Node(
        package='rviz2',
        executable='rviz2',

        name='rviz2',

        output='screen',

        arguments=[
            '-d',
            rviz_config
        ],

        parameters=[
            {
                'use_sim_time': True,
            }
        ]
    )

    # ============================================================
    # RETURN
    # ============================================================

    return LaunchDescription([

        # Robot TF
        robot_state_publisher,

        # Joint visualization
        joint_state_publisher_gui,

        # RViz
        rviz,
    ])