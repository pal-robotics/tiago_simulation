# TIAGo RTAB-Map SLAM

This package provides a comprehensive implementation of RTAB-Map SLAM for the TIAGo robot, supporting both simulation and real-world deployment.

## Overview

RTAB-Map (Real-Time Appearance-Based Mapping) is a powerful RGB-D Graph-based SLAM approach based on an incremental appearance-based loop closure detector. This implementation is specifically configured for TIAGo robot's sensor setup including:

- Xtion RGB-D camera
- Laser range finder
- Wheel odometry
- IMU data (optional)

## Features

- **Real-time SLAM**: RGB-D visual SLAM with loop closure detection
- **2D/3D Mapping**: Generate both 2D occupancy grids and 3D point cloud maps
- **Localization Mode**: Switch between mapping and localization modes
- **Navigation Integration**: Full integration with ROS 2 Navigation Stack
- **Data Management**: Automatic map saving and database management
- **Simulation Support**: Complete Gazebo simulation environment
- **Real Robot Support**: Ready for deployment on real TIAGo hardware

## Requirements

### Software Dependencies

```bash
# Core ROS 2 packages (if using ROS 2 distribution)
sudo apt install ros-humble-rtabmap-ros
sudo apt install ros-humble-pointcloud-to-laserscan
sudo apt install ros-humble-laser-filters
sudo apt install ros-humble-nav2-map-server

# Additional dependencies
sudo apt install ros-humble-cv-bridge
sudo apt install ros-humble-image-transport
sudo apt install ros-humble-tf2-ros
```

### Hardware Requirements

For real robot deployment:
- TIAGo robot with Xtion RGB-D camera
- Minimum 8GB RAM recommended
- NVIDIA GPU recommended for optimal performance

For simulation:
- Minimum 4GB RAM
- OpenGL 3.3+ support

## Installation

1. **Create workspace and clone repositories:**
```bash
mkdir -p ~/tiago_ws/src
cd ~/tiago_ws/src

# Clone this package
git clone <this-repository> tiago_rtabmap_slam

# Clone TIAGo simulation packages (if needed)
git clone https://github.com/pal-robotics/tiago_simulation.git
```

2. **Install dependencies:**
```bash
cd ~/tiago_ws
rosdep install --from-paths src --ignore-src -r -y
```

3. **Build the workspace:**
```bash
cd ~/tiago_ws
colcon build --symlink-install
source install/setup.bash
```

## Quick Start

### Simulation Mode

1. **Launch TIAGo simulation with RTAB-Map:**
```bash
ros2 launch tiago_rtabmap_slam tiago_gazebo_rtabmap.launch.py
```

2. **Control the robot to explore:**
```bash
# Use keyboard control
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# Or use navigation goals in RViz
```

3. **Save the map:**
```bash
# Manual save
ros2 service call /map_saver/save_map nav2_msgs/srv/SaveMap "{map_topic: /map, map_url: my_map, image_format: pgm, map_mode: trinary, free_thresh: 0.25, occupied_thresh: 0.65}"
```

### Real Robot Mode

1. **Launch on real TIAGo:**
```bash
ros2 launch tiago_rtabmap_slam tiago_rtabmap_slam.launch.py use_sim_time:=false
```

2. **Start mapping:**
```bash
# The system starts in mapping mode by default
# Drive the robot around to build the map
```

3. **Switch to localization mode:**
```bash
ros2 launch tiago_rtabmap_slam tiago_rtabmap_slam.launch.py localization:=true
```

## Configuration

### RTAB-Map Parameters

Key parameters in `launch/tiago_rtabmap_slam.launch.py`:

```python
# Memory management
'Mem/IncrementalMemory': 'true'     # Enable incremental memory
'Mem/InitWMWithAllNodes': 'false'   # Don't load all nodes at start

# Visual odometry
'RGBD/AngularUpdate': '0.1'         # Minimum angular motion (rad)
'RGBD/LinearUpdate': '0.1'          # Minimum linear motion (m)

# Loop closure
'RGBD/NeighborLinkRefining': 'true' # Refine neighbor links
'RGBD/ProximityBySpace': 'true'     # Use spatial proximity

# 2D SLAM mode
'Reg/Force3DoF': 'true'             # Force 3DoF registration
'Optimizer/Slam2D': 'true'          # 2D SLAM optimization
```

### Sensor Configuration

The package is configured for TIAGo's sensor setup:

- **RGB Camera**: `/xtion/rgb/image_raw`
- **Depth Camera**: `/xtion/depth/image_raw`
- **Laser Scan**: `/scan_filtered`
- **Odometry**: `/mobile_base_controller/odom`

## Usage Examples

### 1. Basic Mapping

```bash
# Start simulation and mapping
ros2 launch tiago_rtabmap_slam tiago_gazebo_rtabmap.launch.py

# In another terminal, control the robot
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/mobile_base_controller/cmd_vel

# Save map when done
ros2 run tiago_rtabmap_slam map_saver.py --filename my_office_map
```

### 2. Advanced Configuration

```bash
# Custom database location
ros2 launch tiago_rtabmap_slam tiago_rtabmap_slam.launch.py \
    database_path:=/home/user/maps/office.db

# Disable RViz for headless operation
ros2 launch tiago_rtabmap_slam tiago_rtabmap_slam.launch.py \
    launch_rviz:=false

# Custom RTAB-Map parameters
ros2 launch tiago_rtabmap_slam tiago_rtabmap_slam.launch.py \
    rtabmap_args:="Kp/MaxFeatures=400,SURF/HessianThreshold=100"
```

### 3. Data Collection and Analysis

```bash
# Launch with data collection
ros2 launch tiago_rtabmap_slam tiago_rtabmap_slam.launch.py
ros2 run tiago_rtabmap_slam data_collector.py

# View collected data
rtabmap-databaseViewer ~/tiago_rtabmap.db
```

## Troubleshooting

### Common Issues

1. **No loop closures detected:**
   - Ensure good lighting conditions
   - Reduce linear/angular update thresholds
   - Check camera calibration

2. **Poor odometry:**
   - Verify wheel odometry calibration
   - Check for wheel slippage
   - Consider visual odometry backup

3. **High memory usage:**
   - Reduce `Kp/MaxFeatures` parameter
   - Enable `Mem/STMSize` limit
   - Use `Mem/RehearsalSimilarity` threshold

4. **Simulation performance:**
   - Reduce Gazebo physics update rate
   - Lower camera resolution/frame rate
   - Disable unnecessary sensors

### Debug Commands

```bash
# Check topic connections
ros2 topic list | grep rtabmap
ros2 topic echo /rtabmap/info

# Monitor CPU/memory usage
htop

# Verify transforms
ros2 run tf2_tools view_frames.py
ros2 run tf2_ros tf2_monitor

# Check service availability
ros2 service list | grep rtabmap
```

## API Reference

### Launch Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_sim_time` | bool | true | Use simulation time |
| `database_path` | string | ~/tiago_rtabmap.db | RTAB-Map database path |
| `launch_rviz` | bool | true | Launch RViz visualization |
| `localization` | bool | false | Start in localization mode |
| `rtabmap_args` | string | "" | Additional RTAB-Map parameters |

### Topics

#### Subscribed Topics
- `/xtion/rgb/image_raw` (sensor_msgs/Image)
- `/xtion/depth/image_raw` (sensor_msgs/Image)
- `/scan_filtered` (sensor_msgs/LaserScan)
- `/mobile_base_controller/odom` (nav_msgs/Odometry)

#### Published Topics
- `/map` (nav_msgs/OccupancyGrid)
- `/rtabmap/cloud_map` (sensor_msgs/PointCloud2)
- `/rtabmap/global_path` (nav_msgs/Path)
- `/rtabmap_status` (std_msgs/String)

### Services

- `/rtabmap/reset` (std_srvs/Empty)
- `/rtabmap/pause` (std_srvs/Empty)
- `/rtabmap/resume` (std_srvs/Empty)
- `/rtabmap/set_mode_mapping` (std_srvs/Empty)
- `/rtabmap/set_mode_localization` (std_srvs/Empty)

## Performance Optimization

### For Real-time Performance

1. **Reduce visual features:**
```python
'Kp/MaxFeatures': '200'
'SURF/HessianThreshold': '200'
```

2. **Optimize memory usage:**
```python
'Mem/STMSize': '30'
'Mem/RehearsalSimilarity': '0.6'
```

3. **Adjust update rates:**
```python
'RGBD/LinearUpdate': '0.2'
'RGBD/AngularUpdate': '0.2'
```

### For Map Quality

1. **Increase features:**
```python
'Kp/MaxFeatures': '600'
'SURF/HessianThreshold': '100'
```

2. **Enable all sensors:**
```python
'Grid/Sensor': '1'  # Use laser + RGB-D
'Grid/RayTracing': 'true'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This package is licensed under the Apache 2.0 License. See LICENSE file for details.

## Support

For questions and support:
- Create an issue on the repository
- Check the [RTAB-Map documentation](http://wiki.ros.org/rtabmap_ros)
- Visit the [TIAGo documentation](http://wiki.ros.org/Robots/TIAGo)

## References

- [RTAB-Map: Real-Time Appearance-Based Mapping](http://introlab.github.io/rtabmap/)
- [TIAGo Robot Documentation](http://wiki.ros.org/Robots/TIAGo)
- [ROS 2 Navigation Stack](https://navigation.ros.org/)