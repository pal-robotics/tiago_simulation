@[if ft_sensor == "schunk-ft" or end_effector == "schunk-wsg"]@
force_torque:
@[end if]@
@[if ft_sensor == "schunk-ft"]@
  wrist_ft:
    sensor_joint: arm_7_joint
    frame: wrist_ft_link
@[end if]@
@[if end_effector == "schunk-wsg"]@
  left_fingertip:
    sensor_joint: gripper_left_finger_joint
    frame: gripper_left_fingertip_link
  right_fingertip:
    sensor_joint: gripper_right_finger_joint
    frame: gripper_right_fingertip_link
@[end if]@

imu:
  base_imu:
    frame: base_imu_link
    gazebo_sensor_name: imu_sensor

