#!/usr/bin/env python

import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState

joint_names = ["gripper_left_finger_joint", "gripper_right_finger_joint"]
closed  = [0.045, 0.045]

if __name__ == "__main__":
  rospy.init_node("home_gripper")
  rospy.loginfo("Waiting for gripper_controller...")
  client = actionlib.SimpleActionClient("gripper_controller/follow_joint_trajectory", FollowJointTrajectoryAction)
  client.wait_for_server()
  rospy.loginfo("...connected.")

  rospy.wait_for_message("/joint_states", JointState)

  trajectory = JointTrajectory()
  trajectory.joint_names = joint_names
  trajectory.points.append(JointTrajectoryPoint())
  trajectory.points[0].positions = closed
  trajectory.points[0].velocities = [0.0 for i in joint_names]
  trajectory.points[0].accelerations = [0.0 for i in joint_names]
  trajectory.points[0].time_from_start = rospy.Duration(2.0)

  rospy.loginfo("Opening gripper...")
  goal = FollowJointTrajectoryGoal()
  goal.trajectory = trajectory
  goal.goal_time_tolerance = rospy.Duration(0.0)

  client.send_goal(goal)
  client.wait_for_result(rospy.Duration(3.0))
  rospy.loginfo("Gripper opened.")
