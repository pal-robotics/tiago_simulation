///////////////////////////////////////////////////////////////////////////////
// Copyright (C) 2015, PAL Robotics S.L.
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

#include <cassert>
#include <boost/foreach.hpp>

#include <gazebo/sensors/SensorManager.hh>

#include <urdf_parser/urdf_parser.h>

#include <joint_limits_interface/joint_limits_urdf.h>
#include <joint_limits_interface/joint_limits_rosparam.h>

#include <tiago_hardware_gazebo/tiago_hardware_gazebo.h>

using std::string;
using std::vector;

namespace tiago_hardware_gazebo
{
  using namespace hardware_interface;

  TiagoHardwareGazebo::TiagoHardwareGazebo()
    : gazebo_ros_control::RobotHWSim()
  {}


  bool TiagoHardwareGazebo::initSim(const std::string& robot_namespace,
      ros::NodeHandle nh,
      gazebo::physics::ModelPtr model,
      const urdf::Model* const urdf_model,
      std::vector<transmission_interface::TransmissionInfo> transmissions)
  {
    using gazebo::physics::JointPtr;

    // Cleanup
    pos_sim_joints_.clear();
    vel_sim_joints_.clear();
    sim_joints_.clear();
    jnt_pos_.clear();
    jnt_vel_.clear();
    jnt_eff_.clear();
    jnt_pos_cmd_.clear();
    jnt_pos_cmd_curr_.clear();
    jnt_vel_cmd_.clear();

    // Simulation joints
    std::vector<gazebo::physics::JointPtr> sim_joints_tmp = model->GetJoints();

    std::vector<std::string> pos_jnt_names;
    std::vector<std::string> vel_jnt_names;
    std::vector<std::string> jnt_names;
    for (size_t i = 0; i < sim_joints_tmp.size(); ++i)
    {

      // NOTE: This loop has a bunch of tricks that will get removed once automatic transmission parsing is implemented
      const std::string unscoped_name = sim_joints_tmp[i]->GetName();//.substr(7); // NOTE: Removing extra scoping, TODO: Fix!
      if ( !(unscoped_name.size() >= 6 && 0 == unscoped_name.compare(0, 6, "caster")) )
      {
        if(0 == unscoped_name.compare(0, 5, "wheel"))
        {
          boost::shared_ptr<const urdf::Joint> joint(urdf_model->getJoint(unscoped_name));
          if(!joint)
          {
            ROS_ERROR_STREAM(unscoped_name
                             << " couldn't be retrieved from model description");
            return false;
          }

          sim_joints_tmp[i]->SetMaxForce(0u, joint->limits->effort);
          vel_sim_joints_.push_back(sim_joints_tmp[i]);
          vel_jnt_names.push_back(unscoped_name);
        }
        else
        {
          pos_sim_joints_.push_back(sim_joints_tmp[i]);
          pos_jnt_names.push_back(unscoped_name);
        }
      }

      sim_joints_.push_back(sim_joints_tmp[i]);
      jnt_names.push_back(unscoped_name);
    }

    pos_n_dof_ = pos_sim_joints_.size();
    vel_n_dof_ = vel_sim_joints_.size();
    n_dof_ = sim_joints_.size();

    // Raw data
    jnt_pos_.resize(n_dof_);
    jnt_vel_.resize(n_dof_);
    jnt_eff_.resize(n_dof_);
    jnt_pos_cmd_.resize(pos_n_dof_);
    jnt_pos_cmd_curr_.resize(pos_n_dof_);
    jnt_vel_cmd_.resize(vel_n_dof_);

    // Hardware interfaces
    for (size_t i = 0; i < n_dof_; ++i)
    {

      jnt_state_interface_.registerHandle(JointStateHandle(jnt_names[i],
                                                           &jnt_pos_[i],
                                                           &jnt_vel_[i],
                                                           &jnt_eff_[i]));
    }
    for (size_t i = 0; i < pos_n_dof_; ++i)
    {

      jnt_pos_cmd_interface_.registerHandle(JointHandle(jnt_state_interface_.getHandle(pos_jnt_names[i]),
                                                        &jnt_pos_cmd_[i]));
      ROS_DEBUG_STREAM("Registered joint '" << pos_jnt_names[i] << "' in the PositionJointInterface.");
    }
    for (size_t i = 0; i < vel_n_dof_; ++i)
    {

      jnt_vel_cmd_interface_.registerHandle(JointHandle(jnt_state_interface_.getHandle(vel_jnt_names[i]),
                                                        &jnt_vel_cmd_[i]));
      ROS_DEBUG_STREAM("Registered joint '" << pos_jnt_names[i] << "' in the VelocityJointInterface.");
    }
    registerInterface(&jnt_state_interface_);
    registerInterface(&jnt_pos_cmd_interface_);
    registerInterface(&jnt_vel_cmd_interface_);

    // Position joint limits interface
    vector<string> pos_joints_with_limits, pos_joints_without_limits;
    for (size_t i = 0; i < pos_n_dof_; ++i)
    {
      JointHandle cmd_handle = jnt_pos_cmd_interface_.getHandle(pos_sim_joints_[i]->GetName());
      const string name = cmd_handle.getName();

      using namespace joint_limits_interface;
      boost::shared_ptr<const urdf::Joint> urdf_joint = urdf_model->getJoint(name);
      JointLimits limits;
      SoftJointLimits soft_limits;
      if (!getJointLimits(urdf_joint, limits) || !getSoftJointLimits(urdf_joint, soft_limits))
      {
        pos_joints_without_limits.push_back(name);
        continue;
      }
      pos_jnt_limits_interface_.registerHandle(PositionJointSoftLimitsHandle(cmd_handle, limits, soft_limits));
      pos_joints_with_limits.push_back(name);
    }
    if (!pos_joints_with_limits.empty())
    {
      ROS_DEBUG_STREAM("Joint limits will be enforced for position-controlled joints:" <<
                        containerToString(pos_joints_with_limits, "\n - "));
    }
    if (!pos_joints_without_limits.empty())
    {
      ROS_WARN_STREAM("Joint limits will not be enforced for position-controlled joints:" <<
                      containerToString(pos_joints_without_limits, "\n - "));
    }

    // Velocity joint limits interface
    vector<string> vel_joints_with_limits, vel_joints_without_limits;
    for (unsigned int i = 0; i < vel_n_dof_; ++i)
    {
      JointHandle cmd_handle = jnt_vel_cmd_interface_.getHandle(vel_sim_joints_[i]->GetName());
      const string name = cmd_handle.getName();

      using namespace joint_limits_interface;
      boost::shared_ptr<const urdf::Joint> urdf_joint = urdf_model->getJoint(name);
      JointLimits limits;
      if (!getJointLimits(urdf_joint, limits) || !getJointLimits(name, nh, limits))
      {
        vel_joints_without_limits.push_back(name);
        continue;
      }
      vel_jnt_limits_interface_.registerHandle(VelocityJointSaturationHandle(cmd_handle, limits));
      vel_joints_with_limits.push_back(name);
    }
    if (!vel_joints_with_limits.empty())
    {
      ROS_DEBUG_STREAM("Joint limits will be enforced for velocity-controlled joints:" <<
                        containerToString(vel_joints_with_limits, "\n - "));
    }
    if (!vel_joints_without_limits.empty())
    {
      ROS_WARN_STREAM("Joint limits will not be enforced for velocity-controlled joints:" <<
                      containerToString(vel_joints_without_limits, "\n - "));
    }

    // Hardware interfaces: Base IMU sensors
    const string imu_name = "base_imu";
    imu_sensor_  = (gazebo::sensors::ImuSensor*)gazebo::sensors::SensorManager::Instance()->GetSensor(imu_name+"_sensor").get(); // TODO: Fetch from URDF?
    if (!this->imu_sensor_)
    {
      ROS_ERROR_STREAM("Could not find base IMU sensor.");
      return false;
    }

    ImuSensorHandle::Data data;
    data.name     = imu_name;           // TODO: Fetch from elsewhere?
    data.frame_id = imu_name + "_link"; // TODO: Fetch from URDF?
    data.orientation = &base_orientation_[0];
    imu_sensor_interface_.registerHandle(ImuSensorHandle(data));
    registerInterface(&imu_sensor_interface_);
    ROS_DEBUG_STREAM("Registered IMU sensor.");

    // PID controllers
    pids_.resize(pos_n_dof_);
    for (size_t i = 0; i < pos_n_dof_; ++i)
    {
      ros::NodeHandle joint_nh(nh, "gains/" + pos_jnt_names[i]);
      if (!pids_[i].init(joint_nh)) {return false;}
    }

    return true;
  }

  void TiagoHardwareGazebo::readSim(ros::Time time, ros::Duration period)
  {
    for(unsigned int j = 0; j < n_dof_; ++j)
    {
      // Gazebo has an interesting API...
      jnt_pos_[j] += angles::shortest_angular_distance
          (jnt_pos_[j], sim_joints_[j]->GetAngle(0u).Radian());
      jnt_vel_[j] = sim_joints_[j]->GetVelocity(0u);
      jnt_eff_[j] = sim_joints_[j]->GetForce(0u);
    }

    // TODO: Implement ina cleaner way
    for(unsigned int j = 0; j < pos_n_dof_; ++j)
    {
      jnt_pos_cmd_curr_[j] += angles::shortest_angular_distance
          (jnt_pos_cmd_curr_[j], pos_sim_joints_[j]->GetAngle(0u).Radian());
    }

    // Read IMU sensor
    gazebo::math::Quaternion imu_quat = imu_sensor_->GetOrientation();
    base_orientation_[0] = imu_quat.x;
    base_orientation_[1] = imu_quat.y;
    base_orientation_[2] = imu_quat.z;
    base_orientation_[3] = imu_quat.w;

    gazebo::math::Vector3 imu_ang_vel = imu_sensor_->GetAngularVelocity();
    base_ang_vel_[0] = imu_ang_vel.x;
    base_ang_vel_[1] = imu_ang_vel.y;
    base_ang_vel_[2] = imu_ang_vel.z;

    gazebo::math::Vector3 imu_lin_acc = imu_sensor_->GetLinearAcceleration();
    base_lin_acc_[0] =  imu_lin_acc.x;
    base_lin_acc_[1] =  imu_lin_acc.y;
    base_lin_acc_[2] =  imu_lin_acc.z;
  }

  void TiagoHardwareGazebo::writeSim(ros::Time time, ros::Duration period)
  {
    // Enforce joint limits
    pos_jnt_limits_interface_.enforceLimits(period);
    vel_jnt_limits_interface_.enforceLimits(period);

    // Compute and send commands
    for(unsigned int j = 0; j < pos_n_dof_; ++j)
    {
      const double error = jnt_pos_cmd_[j] - jnt_pos_cmd_curr_[j];
      const double effort = pids_[j].computeCommand(error, period);

      // Gazebo has an interesting API...
      pos_sim_joints_[j]->SetForce(0u, effort);
    }
    for(unsigned int j = 0; j < vel_n_dof_; ++j)
    {
      // Gazebo has an interesting API...
      vel_sim_joints_[j]->SetVelocity(0u, jnt_vel_cmd_[j]);
    }
  }

} // tiago_hardware_gazebo

PLUGINLIB_EXPORT_CLASS( tiago_hardware_gazebo::TiagoHardwareGazebo, gazebo_ros_control::RobotHWSim)
