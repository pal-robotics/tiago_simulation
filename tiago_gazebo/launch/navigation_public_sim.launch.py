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

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.substitutions import FindPackageShare
from launch_pal.robot_arguments import CommonArgs
from launch_pal.arg_utils import LaunchArgumentsBase
from launch_pal.include_utils import include_scoped_launch_py_description


@dataclass(frozen=True)
class LaunchArguments(LaunchArgumentsBase):
    world_name: DeclareLaunchArgument = CommonArgs.world_name
    slam: DeclareLaunchArgument = CommonArgs.slam
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
    public_nav_params = PathJoinSubstitution([
        FindPackageShare(PythonExpression(["'", LaunchConfiguration('base_type'), "'_2dnav"])),
        'config',
        'nav_public_sim.yaml',
    ])

    # Navigation
    navigation = include_scoped_launch_py_description(
        pkg_name='nav2_bringup',
        paths=['launch', 'navigation_launch.py'],
        launch_arguments={
            'params_file': public_nav_params,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
    )

    launch_description.add_action(navigation)

    # Localization
    localization = include_scoped_launch_py_description(
        pkg_name='nav2_bringup',
        paths=['launch', 'localization_launch.py'],
        launch_arguments={
            'params_file': public_nav_params,
            'map': PathJoinSubstitution([
                get_package_share_directory('pal_maps'),
                'maps',
                LaunchConfiguration('world_name'),
                'map.yaml'
            ]),
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'world_name': LaunchConfiguration('world_name'),
        },
        condition=UnlessCondition(LaunchConfiguration('slam')),
    )

    launch_description.add_action(localization)

    # SLAM
    slam = include_scoped_launch_py_description(
        pkg_name='nav2_bringup',
        paths=['launch', 'slam_launch.py'],
        launch_arguments={
            'params_file': public_nav_params,
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        },
        condition=IfCondition(LaunchConfiguration('slam')),
    )

    launch_description.add_action(slam)

    # RViz
    rviz = include_scoped_launch_py_description(
        pkg_name='nav2_bringup',
        paths=['launch', 'rviz_launch.py'],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    launch_description.add_action(rviz)
