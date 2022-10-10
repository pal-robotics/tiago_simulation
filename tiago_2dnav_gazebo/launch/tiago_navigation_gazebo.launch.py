# Copyright (c) 2022 PAL Robotics S.L. All rights reserved.
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

from launch import LaunchDescription
from launch_pal.include_utils import include_launch_py_description


def generate_launch_description():

    tiago_gazebo_launch = include_launch_py_description(
        'tiago_gazebo', ['launch', 'tiago_gazebo.launch.py'],
    )

    tiago_nav_bringup_launch = include_launch_py_description(
        'tiago_2dnav', ['launch', 'tiago_nav_bringup.launch.py'],
        launch_arguments={
            'slam': 'False'
        }.items())

    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(tiago_gazebo_launch)
    ld.add_action(tiago_nav_bringup_launch)

    return ld
