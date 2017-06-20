#! /bin/sh
#
# Check if the $HOME/.pal folder is available and creates it if needed before
# launching navigation and amcl.
#
# Usage: $0 [<robot_name>] [<x_pose>] [<y_pose>]

# Check parameters:
if [ $# -lt 1 ]; then
  ROBOT_FILE=pose.yaml
else
  ROBOT_FILE=$1_pose.yaml
fi

if [ $# -lt 2 ]; then
  X_POSE=0.0
else
  X_POSE=$2
fi

if [ $# -lt 3 ]; then
  Y_POSE=0.0
else
  Y_POSE=$3
fi

# Ensure target directory exists
MAP=$HOME/.pal
if [ ! -d "$MAP" ]; then
  mkdir -p $MAP
  if [ $? -ne 0 ]; then
   echo "Error: Failed to create path $MAP"
    exit 3
  fi
fi

# Write the pose file
echo "{initial_cov_aa: 0.02, initial_cov_xx: 0.01, initial_cov_yy: 0.01, initial_pose_a: 0.0,
  initial_pose_x: $X_POSE, initial_pose_y: $Y_POSE}" > $MAP/$ROBOT_FILE



