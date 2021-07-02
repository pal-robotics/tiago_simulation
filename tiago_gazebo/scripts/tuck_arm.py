#!/usr/bin/env python3

# Copyright 2021 PAL Robotics S.L.
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

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from play_motion_msgs.action import PlayMotion


class PlayMotionActionClient(Node):

    def __init__(self):
        super().__init__('play_motion_action_client')
        self._action_client = ActionClient(self, PlayMotion, 'play_motion')

    def send_goal(self, motion_name, skip_planning):
        goal_msg = PlayMotion.Goal()
        goal_msg.motion_name = motion_name
        goal_msg.skip_planning = skip_planning

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()

        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: error code ({}): {}'.format(
            result.error_code, result.error_string))
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    action_client = PlayMotionActionClient()

    action_client.send_goal('home', True)

    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
