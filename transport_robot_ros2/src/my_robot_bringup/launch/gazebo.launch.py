#!/usr/bin/env python3

import os

import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    # =========================================================
    # PACKAGE DIRECTORIES
    # =========================================================

    robot_description_pkg = get_package_share_directory(
        'my_robot_description'
    )

    bringup_pkg = get_package_share_directory(
        'my_robot_bringup'
    )

    ros_gz_sim_pkg = get_package_share_directory(
        'ros_gz_sim'
    )

    # Parent directory of the description package.
    #
    # Example:
    # /home/rostheboss/transport_robot_ros2/install
    #
    robot_description_parent = os.path.dirname(
        robot_description_pkg
    )

    # =========================================================
    # WORLD FILE
    # =========================================================
    #
    # The world is now stored inside the ROS 2 package:
    #
    # my_robot_bringup/worlds/transport_world.sdf
    #
    # This makes the repository portable and removes the
    # dependency on ~/sdf_test/test_11x11.sdf
    #
    # =========================================================

    world_file = os.path.join(
        bringup_pkg,
        'worlds',
        'transport_world.sdf'
    )

    if not os.path.isfile(world_file):
        raise FileNotFoundError(
            f'\nGazebo world not found:\n{world_file}\n'
        )

    print(f'Using Gazebo world:\n{world_file}')

    # =========================================================
    # GAZEBO RESOURCE PATH
    # =========================================================
    #
    # Allows Gazebo to find resources from the installed
    # ROS 2 packages and the world directory.
    #
    # =========================================================

    existing_resource_path = os.environ.get(
        'GZ_SIM_RESOURCE_PATH',
        ''
    )

    resource_paths = [
        robot_description_parent,
        bringup_pkg,
        os.path.dirname(world_file),
    ]

    # Keep existing Gazebo resource paths if they exist.
    if existing_resource_path:
        resource_paths.append(existing_resource_path)

    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.pathsep.join(resource_paths)
    )

    # =========================================================
    # XACRO FILE
    # =========================================================

    xacro_file = os.path.join(
        robot_description_pkg,
        'urdf',
        'transport_robot.xacro'
    )

    if not os.path.isfile(xacro_file):
        raise FileNotFoundError(
            f'\nTransport robot Xacro not found:\n{xacro_file}\n'
        )

    # =========================================================
    # PROCESS XACRO
    # =========================================================

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

    # =========================================================
    # START GAZEBO SIM
    # =========================================================

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                ros_gz_sim_pkg,
                'launch',
                'gz_sim.launch.py'
            )
        ),

        launch_arguments={
            # -r = start simulation immediately
            'gz_args': f'-r {world_file}'
        }.items()
    )

    # =========================================================
    # ROBOT STATE PUBLISHER
    # =========================================================

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

    # =========================================================
    # SPAWN ROBOT INTO GAZEBO
    # =========================================================

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',

        name='spawn_transport_robot',

        output='screen',

        arguments=[

            '-topic',
            'robot_description',

            '-name',
            'transport_robot',

            # =================================================
            # INITIAL POSITION
            # =================================================

            '-x',
            '5.1',

            '-y',
            '-5.2',

            '-z',
            '0.15',

            # =================================================
            # INITIAL ORIENTATION
            # =================================================

            '-R',
            '0.0',

            '-P',
            '0.0',

            '-Y',
            '1.57',
        ]
    )

    # =========================================================
    # GAZEBO <-> ROS 2 BRIDGE
    # =========================================================

    bridge_file = os.path.join(
        bringup_pkg,
        'config',
        'tr_gazebo_bridge.yaml'
    )

    if not os.path.isfile(bridge_file):
        raise FileNotFoundError(
            f'\nGazebo bridge configuration not found:\n'
            f'{bridge_file}\n'
        )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',

        name='ros_gz_bridge',

        output='screen',

        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_file}',
        ]
    )

    # =========================================================
    # RETURN LAUNCH DESCRIPTION
    # =========================================================

    return LaunchDescription([

        # Gazebo resource paths
        gazebo_resource_path,

        # Gazebo
        gazebo,

        # Robot TF
        robot_state_publisher,

        # Spawn robot
        spawn_robot,

        # ROS <-> Gazebo bridge
        bridge,
    ])