#!/usr/bin/env python3

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

import time

from play_motion2_msgs.action import PlayMotion2
from play_motion2_msgs.srv import IsMotionReady

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


class PlayMotionActionClient(Node):

    def __init__(self):
        super().__init__('arm_tucker')
        self._play_motion_client = ActionClient(
            self, PlayMotion2, 'play_motion2')
        self._is_ready_client = self.create_client(
            IsMotionReady, '/play_motion2/is_motion_ready')
        self._is_successful = None

    def is_successful(self):
        return self._is_successful

    def wait_for_server(self):
        self._play_motion_client.wait_for_server()

        while not self._is_ready_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('is_ready service not ready, waiting...')

        request = IsMotionReady.Request()
        request.motion_key = 'home'

        is_ready = False
        while not is_ready:
            time.sleep(3.0)
            future = self._is_ready_client.call_async(request)
            while rclpy.ok() and not is_ready:
                rclpy.spin_once(self)
                if future.done():
                    try:
                        response = future.result()
                    except Exception as e:
                        self.get_logger().info('Service call failed %r' % (e,))
                    else:
                        is_ready = response.is_ready
                        if is_ready:
                            self.get_logger().info('play_motion2 is ready')
                        else:
                            self.get_logger().error('play_motion2 is not ready')
                    break

    def send_goal(self, motion_name, skip_planning):
        goal_msg = PlayMotion2.Goal()
        goal_msg.motion_name = motion_name
        goal_msg.skip_planning = skip_planning

        self._send_goal_future = \
            self._play_motion_client.send_goal_async(goal_msg)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

        rclpy.spin_until_future_complete(self, self._send_goal_future)

        while self._is_successful is None:
            time.sleep(1.0)
            rclpy.spin_once(self)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self._is_successful = False
            self.get_logger().error('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()

        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result

        error = result.error

        if error == '':
            self._is_successful = True
            self.get_logger().info('Motion succeeded')
        else:
            self._is_successful = False
            self.get_logger().error(
                'Motion failed with error {}'
                .format(error))


def main(args=None):
    rclpy.init(args=args)

    action_client = PlayMotionActionClient()

    action_client.wait_for_server()

    for i in range(5):
        action_client.get_logger().info('Tucking arm... Try {}'.format(i))
        action_client.send_goal('home', True)

        if action_client.is_successful():
            action_client.get_logger().info('Arm tucked')
            break
        else:
            action_client.get_logger().error('Tuck failed')

        time.sleep(5)

    if not action_client.is_successful():
        action_client.get_logger().error('Failed to tuck arm after 5 tries')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
