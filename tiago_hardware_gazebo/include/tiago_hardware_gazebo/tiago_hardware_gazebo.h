///////////////////////////////////////////////////////////////////////////////
// Copyright (C) 2013, PAL Robotics S.L.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//   * Redistributions of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//   * Redistributions in binary form must reproduce the above copyright
//     notice, this list of conditions and the following disclaimer in the
//     documentation and/or other materials provided with the distribution.
//   * Neither the name of PAL Robotics S.L. nor the names of its
//     contributors may be used to endorse or promote products derived from
//     this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
//////////////////////////////////////////////////////////////////////////////

#ifndef ANT_HARDWARE_GAZEBO_ANT_HARDWARE_GAZEBO_H
#define ANT_HARDWARE_GAZEBO_ANT_HARDWARE_GAZEBO_H

#include <vector>
#include <string>

#include <control_toolbox/pid.h>

#include <hardware_interface/robot_hw.h>
#include <hardware_interface/joint_state_interface.h>
#include <hardware_interface/joint_command_interface.h>
#include <hardware_interface/imu_sensor_interface.h>
#include <joint_limits_interface/joint_limits_interface.h>

#include <pluginlib/class_list_macros.h>

#include <gazebo_ros_control/robot_hw_sim.h>

#include <angles/angles.h>

#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/sensors/ImuSensor.hh>
#include <gazebo/common/common.hh>

namespace tiago_hardware_gazebo
{

class TiagoHardwareGazebo : public gazebo_ros_control::RobotHWSim
{
public:

  TiagoHardwareGazebo();

  // Simulation-specific
  bool initSim(const std::string& robot_namespace,
      ros::NodeHandle model_nh,
      gazebo::physics::ModelPtr parent_model,
      const urdf::Model* const urdf_model,
      std::vector<transmission_interface::TransmissionInfo> transmissions);
  void readSim(ros::Time time, ros::Duration period);
  void writeSim(ros::Time time, ros::Duration period);


private:
  // Raw data
  unsigned int pos_n_dof_;
  unsigned int vel_n_dof_;
  unsigned int n_dof_;

  std::vector<std::string> transmission_names_;

  std::vector<double> jnt_pos_;
  std::vector<double> jnt_vel_;
  std::vector<double> jnt_eff_;

  std::vector<double> jnt_pos_cmd_;
  std::vector<double> jnt_pos_cmd_curr_; // NOTE: This is the same as jnt_pos_ but only with the joints in pos_sim_joints_. Needs cleaner implementation

  std::vector<double> jnt_vel_cmd_;

  double base_orientation_[4];
  double base_ang_vel_[3];
  double base_lin_acc_[3];

  // Simulation-specific
  std::vector<gazebo::physics::JointPtr> sim_joints_;
  std::vector<gazebo::physics::JointPtr> pos_sim_joints_;
  std::vector<gazebo::physics::JointPtr> vel_sim_joints_;
  gazebo::sensors::ImuSensor* imu_sensor_;

  // Hardware interface: joints
  hardware_interface::JointStateInterface    jnt_state_interface_;
  hardware_interface::PositionJointInterface jnt_pos_cmd_interface_;
  hardware_interface::VelocityJointInterface jnt_vel_cmd_interface_;

  // Hardware interface: sensors
  hardware_interface::ImuSensorInterface     imu_sensor_interface_; // For inclinometer

  // Joint limits interface
  joint_limits_interface::PositionJointSoftLimitsInterface pos_jnt_limits_interface_;
  joint_limits_interface::VelocityJointSaturationInterface vel_jnt_limits_interface_;

  // PID controllers
  std::vector<control_toolbox::Pid> pids_;

  template <class T>
  std::string containerToString(const T& cont, const std::string& prefix)
  {
    std::stringstream ss;
    ss << prefix;
    std::copy(cont.begin(), --cont.end(), std::ostream_iterator<typename T::value_type>(ss, prefix.c_str()));
    ss << *(--cont.end());
    return ss.str();
  }

};

}

#endif // ANT_HARDWARE_GAZEBO_ANT_HARDWARE_GAZEBO_H
