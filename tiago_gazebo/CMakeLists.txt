cmake_minimum_required(VERSION 3.4.0)
project(tiago_gazebo)

find_package(ament_cmake_auto REQUIRED)

# PAL Robotics stricter build flags, other developers should not worry about this
find_package(ament_cmake_pal QUIET)

install(
  PROGRAMS scripts/tuck_arm.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# Media commented out
ament_auto_package(INSTALL_TO_SHARE launch models worlds)
