#!/usr/bin/env python

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

import actionlib
from play_motion_msgs.msg import PlayMotionAction, PlayMotionGoal
import rospy
from sensor_msgs.msg import JointState

if __name__ == '__main__':
    rospy.init_node('grasp_demo')
    rospy.loginfo('Waiting for play_motion...')
    client = actionlib.SimpleActionClient('play_motion', PlayMotionAction)
    client.wait_for_server()
    rospy.loginfo('...connected.')

    rospy.wait_for_message('joint_states', JointState)
    rospy.sleep(3.0)

    rospy.loginfo('Grasping demo...')
    goal = PlayMotionGoal()

    goal.motion_name = 'look_at_object_demo'
    goal.skip_planning = True
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration(5.0))

    goal.motion_name = 'pregrasp_demo'
    goal.skip_planning = False
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration(40.0))

    goal.motion_name = 'grasp_demo'
    goal.skip_planning = True
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration(10.0))

    rospy.sleep(1.0)

    goal.motion_name = 'pick_demo'
    goal.skip_planning = False
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration(30.0))

    rospy.loginfo('Grasping demo OK.')
