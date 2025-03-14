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
#include "play_motion2_msgs/srv/get_motion_info.hpp"
#include "rclcpp/executors.hpp"
#include "rclcpp/node.hpp"
#include "rclcpp/wait_for_message.hpp"
#include "sensor_msgs/msg/joint_state.hpp"

using namespace std::chrono_literals;
using IsMotionReady = play_motion2_msgs::srv::IsMotionReady;
using GetMotionInfo = play_motion2_msgs::srv::GetMotionInfo;

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
  auto it = std::find(joint_states.name.cbegin(), joint_states.name.cend(), joint_name);

  // Ensure the joint exists
  ASSERT_NE(
    it,
    joint_states.name.cend()) << "Joint name " << joint_name << " not found in joint_states.";

  auto position = std::distance(joint_states.name.cbegin(), it);

  // Ensure the position index is within valid bounds
  ASSERT_LT(position, joint_states.position.size())
    << "Position index out of range for joint " << joint_name;

  // Perform the position check
  ASSERT_NEAR(joint_states.position.at(position), expected_position, MAX_ABS_ERROR)
    << "Position mismatch for joint " << joint_name;
}


TEST(TuckArmTest, TuckArmTest)
{
  const auto node = rclcpp::Node::make_shared("tuck_arm_test_node");
  // Create clients for the two services
  auto is_motion_ready_client = node->create_client<IsMotionReady>("play_motion2/is_motion_ready");
  auto get_motion_info_client = node->create_client<GetMotionInfo>("play_motion2/get_motion_info");

  ASSERT_TRUE(is_motion_ready_client->wait_for_service(TIMEOUT)) <<
    "Service /play_motion2/is_motion_ready not available.";
  ASSERT_TRUE(get_motion_info_client->wait_for_service(TIMEOUT)) <<
    "Service /play_motion2/get_motion_info not available.";

  // wait until play_motion is ready
  wait_play_motion2_state(node, is_motion_ready_client, play_motion_state::AVAILABLE);

  // wait until play_motion is busy -> tuck_arm execution
  wait_play_motion2_state(node, is_motion_ready_client, play_motion_state::BUSY);

  // wait until play_motion is ready -> tuck_arm finished
  wait_play_motion2_state(node, is_motion_ready_client, play_motion_state::AVAILABLE);

  // Get the expected joint positions from the service
  auto request = std::make_shared<GetMotionInfo::Request>();
  request->motion_key = "home";
  auto future_result = get_motion_info_client->async_send_request(request);
  ASSERT_EQ(
    rclcpp::spin_until_future_complete(
      node,
      future_result), rclcpp::FutureReturnCode::SUCCESS)
    << "Service call to /play_motion2/get_motion_info failed.";

  ASSERT_EQ(future_result.wait_for(TIMEOUT), std::future_status::ready);

  auto motion = future_result.get()->motion;
  // Extract joint names and positions from the motion
  auto joint_names = motion.joints;
  auto joint_positions = motion.positions;

  // Extract only the first position for each joint
  std::vector<double> correct_positions;
  // Select the third row (index 2) as the expected joint positions
  size_t num_positions_per_joint = joint_positions.size() / joint_names.size();
  size_t selected_row = num_positions_per_joint - 1;
  ASSERT_LT(selected_row, num_positions_per_joint) << "Invalid selected row index.";

  for (size_t i = 0; i < joint_names.size(); ++i) {
    correct_positions.push_back(joint_positions[i + (selected_row * joint_names.size())]);
  }

  // Ensure sizes match after extraction
  ASSERT_EQ(joint_names.size(), correct_positions.size())
    << "Mismatch between joint names and extracted positions sizes.";

  // Combine joint names and positions into a map for comparison
  std::map<std::string, double> expected_joint_positions;
  for (size_t i = 0; i < joint_names.size(); ++i) {
    expected_joint_positions[joint_names[i]] =
      joint_positions[i + (selected_row * joint_names.size())];
  }

  // Check joint_states
  sensor_msgs::msg::JointState joint_states;
  bool success = rclcpp::wait_for_message<sensor_msgs::msg::JointState>(
    joint_states, node, "/joint_states");
  ASSERT_TRUE(success) << "Failed to receive joint states from /joint_states topic.";

  // Compare actual joint positions to expected positions from the service
  for (const auto & joint_position : expected_joint_positions) {
    const auto & joint_name = joint_position.first;
    const auto & expected_position = joint_position.second;
    check_joint_position(joint_states, joint_name, expected_position);
  }
}

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  testing::InitGoogleTest();
  const auto ret = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return ret;
}
