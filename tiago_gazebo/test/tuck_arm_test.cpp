// Copyright (c) 2023 PAL Robotics S.L. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <gtest/gtest.h>

#include <thread>

#include "play_motion2_msgs/srv/is_motion_ready.hpp"
#include "rclcpp/executors.hpp"
#include "rclcpp/node.hpp"
#include "rclcpp/wait_for_message.hpp"
#include "sensor_msgs/msg/joint_state.hpp"

using namespace std::chrono_literals;
using IsMotionReady = play_motion2_msgs::srv::IsMotionReady;

const auto TIMEOUT = 10s;
const auto PLAY_MOTION_STATE_TIMEOUT = 30s;
constexpr double MAX_ABS_ERROR = 0.02;

enum play_motion_state
{
  AVAILABLE,
  BUSY,
};

/// wait for play_motion2
/// The value of state is the one we want to wait for
void wait_play_motion2_state(
  rclcpp::Node::SharedPtr node,
  rclcpp::Client<IsMotionReady>::SharedPtr client,
  play_motion_state state)
{
  RCLCPP_INFO_EXPRESSION(
    node->get_logger(), state == play_motion_state::BUSY, "waiting for state BUSY");
  RCLCPP_INFO_EXPRESSION(
    node->get_logger(), state == play_motion_state::AVAILABLE, "waiting for state AVAILABLE");

  auto request = std::make_shared<IsMotionReady::Request>();
  request->motion_key = "home";

  bool timeout = false;
  bool play_motion_state = state;
  auto start_time = node->now();
  do {
    auto future_result = client->async_send_request(request);
    if (rclcpp::spin_until_future_complete(
        node, future_result,
        TIMEOUT) == rclcpp::FutureReturnCode::SUCCESS)
    {
      switch (state) {
        case play_motion_state::AVAILABLE:
          play_motion_state = future_result.get()->is_ready;
          break;
        case play_motion_state::BUSY:
          play_motion_state = !future_result.get()->is_ready;
          break;
      }
    }
    timeout = node->now() - start_time > PLAY_MOTION_STATE_TIMEOUT;

    // sleep to avoid spamming many messages of play_motion2
    std::this_thread::sleep_for(100ms);
  } while (!timeout && !play_motion_state);

  ASSERT_FALSE(timeout) << "Timeout while waiting for play_motion2 state";
}

void check_joint_position(
  const sensor_msgs::msg::JointState & joint_states,
  const std::string & joint_name,
  double expected_position)
{
  auto position =
    std::distance(
    joint_states.name.cbegin(),
    std::find(joint_states.name.cbegin(), joint_states.name.cend(), joint_name));
  ASSERT_NEAR(joint_states.position.at(position), expected_position, MAX_ABS_ERROR);
}

TEST(TuckArmTest, TuckArmTest)
{
  const auto node = rclcpp::Node::make_shared("tuck_arm_test_node");
  auto client = node->create_client<IsMotionReady>(
    "play_motion2/is_motion_ready");

  ASSERT_TRUE(client->wait_for_service(TIMEOUT));

  // wait until play_motion is ready
  wait_play_motion2_state(node, client, play_motion_state::AVAILABLE);

  // wait until play_motion is busy -> tuck_arm execution
  wait_play_motion2_state(node, client, play_motion_state::BUSY);

  // wait until play_motion is ready -> tuck_arm finished
  wait_play_motion2_state(node, client, play_motion_state::AVAILABLE);

  // Check joint_states
  sensor_msgs::msg::JointState joint_states;
  rclcpp::wait_for_message<sensor_msgs::msg::JointState>(
    joint_states,
    node, "/joint_states");

  constexpr double TORSO_LIFT_JOINT_HOME_POS = 0.15;
  check_joint_position(joint_states, "torso_lift_joint", TORSO_LIFT_JOINT_HOME_POS);

  constexpr double ARM_1_JOINT_HOME_POS = 0.20;
  check_joint_position(joint_states, "arm_1_joint", ARM_1_JOINT_HOME_POS);

  constexpr double ARM_2_JOINT_HOME_POS = -1.34;
  check_joint_position(joint_states, "arm_2_joint", ARM_2_JOINT_HOME_POS);

  constexpr double ARM_3_JOINT_HOME_POS = -0.20;
  check_joint_position(joint_states, "arm_3_joint", ARM_3_JOINT_HOME_POS);

  constexpr double ARM_4_JOINT_HOME_POS = 1.94;
  check_joint_position(joint_states, "arm_4_joint", ARM_4_JOINT_HOME_POS);

  constexpr double ARM_5_JOINT_HOME_POS = -1.57;
  check_joint_position(joint_states, "arm_5_joint", ARM_5_JOINT_HOME_POS);

  constexpr double ARM_6_JOINT_HOME_POS = 1.37;
  check_joint_position(joint_states, "arm_6_joint", ARM_6_JOINT_HOME_POS);

  constexpr double ARM_7_JOINT_HOME_POS = 0.0;
  check_joint_position(joint_states, "arm_7_joint", ARM_7_JOINT_HOME_POS);
}

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  testing::InitGoogleTest();
  const auto ret = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return ret;
}
