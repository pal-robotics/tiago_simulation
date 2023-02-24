# Copyright (c) 2023 PAL Robotics S.L. All rights reserved.
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

import os
import unittest
# import subprocess

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
import launch_testing

from launch_pal.include_utils import include_launch_py_description


def generate_test_description():

    tiago_gazebo_dir = get_package_share_directory('tiago_gazebo')

    launch_tiago_gazebo = include_launch_py_description(
        'tiago_gazebo', ['launch', 'tiago_gazebo.launch.py'],
        launch_arguments={'world_name': 'empty_world'}.items())

    tuck_arm_test = launch_testing.actions.GTest(
        path=os.path.join(tiago_gazebo_dir, 'test', 'tuck_arm_test'),
        output='screen')

    ld = LaunchDescription()

    ld.add_action(launch_tiago_gazebo)
    ld.add_action(tuck_arm_test)
    ld.add_action(launch_testing.actions.ReadyToTest())

    context = {'tuck_arm_test': tuck_arm_test}

    return ld, context


class TestStarted(unittest.TestCase):

    # @classmethod
    # def tearDownClass(self):
    #     # gzserver and gzclient aren't always killed on exit
    #     subprocess.call(['pkill gz'], shell=True, stdout=subprocess.PIPE)

    def test_tuck_arm(self, proc_info, proc_output, tuck_arm_test):
        # Wait until process ends
        proc_info.assertWaitForShutdown(process=tuck_arm_test, timeout=120)


@launch_testing.post_shutdown_test()
class TestProcessOutput(unittest.TestCase):

    def test_exit_code(self, proc_info, tuck_arm_test):
        launch_testing.asserts.assertExitCodes(proc_info, process=tuck_arm_test)
