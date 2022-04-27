#!/usr/bin/env python

import rospy
import actionlib
from play_motion_msgs.msg import PlayMotionAction, PlayMotionGoal
from sensor_msgs.msg import JointState

if __name__ == "__main__":
  rospy.init_node("tuck_arm")
  rospy.loginfo("Waiting for play_motion...")
  client = actionlib.SimpleActionClient("play_motion", PlayMotionAction)
  client.wait_for_server()
  rospy.loginfo("...connected.")

  rospy.wait_for_message("joint_states", JointState)
  rospy.sleep(3.0)

  rospy.loginfo("Tuck arm...")
  goal = PlayMotionGoal()
  goal.motion_name = 'home'
  goal.skip_planning = False

  client.send_goal(goal)
  client.wait_for_result(rospy.Duration(10.0))
  rospy.loginfo("Arm tucked.")
