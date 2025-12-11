# Copyright (c) 2025 PAL Robotics S.L. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_pal.substitutions import RobotInfoFile
from launch_pal.robot_arguments import CommonArgs
from launch_pal.arg_utils import LaunchArgumentsBase
from launch_pal.include_utils import include_scoped_launch_py_description
from tiago_description.launch_arguments import TiagoArgs


@dataclass(frozen=True)
class LaunchArguments(LaunchArgumentsBase):
    wheel_model: DeclareLaunchArgument = TiagoArgs.wheel_model
    laser_model: DeclareLaunchArgument = TiagoArgs.laser_model
    base_type: DeclareLaunchArgument = TiagoArgs.base_type
    camera_model: DeclareLaunchArgument = TiagoArgs.camera_model
    navigation: DeclareLaunchArgument = CommonArgs.navigation
    slam: DeclareLaunchArgument = CommonArgs.slam
    advanced_navigation: DeclareLaunchArgument = CommonArgs.advanced_navigation
    docking: DeclareLaunchArgument = CommonArgs.docking
    namespace: DeclareLaunchArgument = CommonArgs.namespace
    use_sim_time: DeclareLaunchArgument = CommonArgs.use_sim_time
    rviz: DeclareLaunchArgument = CommonArgs.rviz


def generate_launch_description():

    # Create the launch description and populate
    ld = LaunchDescription()
    launch_arguments = LaunchArguments()

    launch_arguments.add_to_launch_description(ld)

    declare_actions(ld, launch_arguments)

    return ld


def declare_actions(
    launch_description: LaunchDescription, launch_args: LaunchArguments
):
    robot_name = 'tiago'

    # Robot Info Publisher
    robot_info_ns = PythonExpression([
        "'/", LaunchConfiguration('namespace'),
        "' if '", LaunchConfiguration('namespace'), "' else ''"
    ])
    robot_info_file = RobotInfoFile(
        content={
            'robot_type': robot_name,
            'wheel_model': launch_args.wheel_model,
            'camera_model': launch_args.camera_model,
            'base_type': launch_args.base_type,
            'laser_model': launch_args.laser_model,
            'has_dock': launch_args.docking,
            'advanced_navigation': launch_args.advanced_navigation,
            'namespace': robot_info_ns,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
    )
    robot_info_env = SetEnvironmentVariable(
        name='ROBOT_INFO_PATH',
        value=robot_info_file
    )
    launch_description.add_action(robot_info_env)

    robot_info_publisher = Node(
        namespace=LaunchConfiguration('namespace'),
        package='robot_info_publisher',
        executable='robot_info_publisher',
        name='robot_info_publisher',
        output='screen',
    )
    launch_description.add_action(robot_info_publisher)

    # Laser Sensors
    laser = include_scoped_launch_py_description(
        pkg_name=PythonExpression(["'", LaunchConfiguration('base_type'), "' + '_laser_sensors'"]),
        paths=['launch', 'laser_sim.launch.py'],
        launch_arguments={
            'namespace': launch_args.namespace,
            'wheel_model': launch_args.wheel_model,
            'camera_model': launch_args.camera_model,
            'base_type': launch_args.base_type,
            'laser_model': launch_args.laser_model,
            'docking': launch_args.docking,
            'advanced_navigation': launch_args.advanced_navigation,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
        env_vars=[robot_info_env],
    )

    launch_description.add_action(laser)

    # Navigation
    navigation = include_scoped_launch_py_description(
        pkg_name=PythonExpression(["'", LaunchConfiguration('base_type'), "' + '_2dnav'"]),
        paths=['launch', 'navigation.launch.py'],
        launch_arguments={
            'namespace': launch_args.namespace,
            'wheel_model': launch_args.wheel_model,
            'camera_model': launch_args.camera_model,
            'base_type': launch_args.base_type,
            'laser_model': launch_args.laser_model,
            'docking': launch_args.docking,
            'advanced_navigation': launch_args.advanced_navigation,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
        env_vars=[robot_info_env],
    )

    launch_description.add_action(navigation)

    # Localization
    localization = include_scoped_launch_py_description(
        pkg_name=PythonExpression(["'", LaunchConfiguration('base_type'), "' + '_2dnav'"]),
        paths=['launch', 'localization.launch.py'],
        launch_arguments={
            'namespace': launch_args.namespace,
            'wheel_model': launch_args.wheel_model,
            'camera_model': launch_args.camera_model,
            'base_type': launch_args.base_type,
            'laser_model': launch_args.laser_model,
            'docking': launch_args.docking,
            'advanced_navigation': launch_args.advanced_navigation,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
        env_vars=[robot_info_env],
        condition=UnlessCondition(LaunchConfiguration('slam')),
    )

    launch_description.add_action(localization)

    # SLAM
    slam = include_scoped_launch_py_description(
        pkg_name=PythonExpression(["'", LaunchConfiguration('base_type'), "' + '_2dnav'"]),
        paths=['launch', 'slam.launch.py'],
        launch_arguments={
            'namespace': launch_args.namespace,
            'wheel_model': launch_args.wheel_model,
            'camera_model': launch_args.camera_model,
            'base_type': launch_args.base_type,
            'laser_model': launch_args.laser_model,
            'docking': launch_args.docking,
            'advanced_navigation': launch_args.advanced_navigation,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
        env_vars=[robot_info_env],
        condition=IfCondition(LaunchConfiguration('slam')),
    )

    launch_description.add_action(slam)

    # Docking
    docking = include_scoped_launch_py_description(
        pkg_name=PythonExpression(["'", LaunchConfiguration('base_type'), "' + '_docking'"]),
        paths=['launch', 'docking_sim.launch.py'],
        launch_arguments={
            'namespace': launch_args.namespace,
            'wheel_model': launch_args.wheel_model,
            'camera_model': launch_args.camera_model,
            'base_type': launch_args.base_type,
            'laser_model': launch_args.laser_model,
            'docking': launch_args.docking,
            'has_dock': launch_args.docking,
            'advanced_navigation': launch_args.advanced_navigation,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
        env_vars=[robot_info_env],
        condition=IfCondition(LaunchConfiguration('docking'))
    )

    launch_description.add_action(docking)

    # Stores Server
    stores_server = Node(
        namespace=LaunchConfiguration('namespace'),
        package='pal_stores_server',
        executable='pal_stores_server',
        arguments=[PathJoinSubstitution([
            os.environ['HOME'], '.pal',
            PythonExpression(["'", LaunchConfiguration('namespace'), "stores.db'"]),
        ])],
        condition=IfCondition(LaunchConfiguration('advanced_navigation'))
    )

    launch_description.add_action(stores_server)

    # Advanced Navigation
    advanced_navigation = include_scoped_launch_py_description(
        pkg_name=PythonExpression([
            "'", LaunchConfiguration('base_type'), "' + '_advanced_2dnav'"
        ]),
        paths=['launch', 'advanced_navigation.launch.py'],
        launch_arguments={
            'namespace': launch_args.namespace,
            'wheel_model': launch_args.wheel_model,
            'camera_model': launch_args.camera_model,
            'base_type': launch_args.base_type,
            'laser_model': launch_args.laser_model,
            'has_dock': launch_args.docking,
            'docking': launch_args.docking,
            'advanced_navigation': launch_args.advanced_navigation,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
        env_vars=[robot_info_env],
        condition=IfCondition(LaunchConfiguration('advanced_navigation'))
    )

    launch_description.add_action(advanced_navigation)

    # RGBD Sensors
    rgbd = include_scoped_launch_py_description(
        pkg_name='tiago_rgbd_sensors',
        paths=['launch', 'rgbd_sim.launch.py'],
        launch_arguments={
            'namespace': launch_args.namespace,
            'wheel_model': launch_args.wheel_model,
            'camera_model': launch_args.camera_model,
            'base_type': launch_args.base_type,
            'laser_model': launch_args.laser_model,
            'docking': launch_args.docking,
            'advanced_navigation': launch_args.advanced_navigation,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
        env_vars=[robot_info_env],
    )

    launch_description.add_action(rgbd)

    # RViz
    rviz_cfg_pkg = PythonExpression([
        "'", LaunchConfiguration('base_type'),
        "' + '_advanced_2dnav' if '",
        LaunchConfiguration('advanced_navigation'),
        "'=='True' else '",
        LaunchConfiguration('base_type'),
        "' + '_2dnav'"
    ])
    rviz = Node(
        namespace=LaunchConfiguration('namespace'),
        package='rviz2',
        executable='rviz2',
        arguments=['-d', PathJoinSubstitution([
            FindPackageShare(rviz_cfg_pkg),
            'config',
            'rviz',
            'navigation.rviz',
        ])],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        output='screen',
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static'),
        ],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    launch_description.add_action(rviz)
