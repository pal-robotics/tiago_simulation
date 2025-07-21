# TIAGo RTAB-Map SLAM - Complete Setup Guide

This guide provides step-by-step instructions for implementing RTAB-Map SLAM with the TIAGo robot, covering both simulation and real-world deployment.

## 🎯 Project Overview

This implementation provides:
- **Complete RTAB-Map SLAM integration** for TIAGo robot
- **Simulation environment** for testing and development
- **Real robot support** for actual deployment
- **Custom visualization** and monitoring tools
- **Navigation integration** for autonomous operation

## 📋 Prerequisites

### System Requirements

**For Simulation:**
- Ubuntu 20.04+ (22.04 recommended)
- 8GB RAM minimum (16GB recommended)
- OpenGL 3.3+ support
- Python 3.8+

**For Real Robot:**
- TIAGo robot with Xtion RGB-D camera
- Ubuntu 20.04+ on robot computer
- Network connection between development machine and robot

### Software Dependencies

```bash
# Essential development tools
sudo apt update
sudo apt install -y python3-pip python3-venv python3-dev
sudo apt install -y cmake pkg-config git

# Computer vision and robotics libraries
sudo apt install -y libopencv-dev
sudo apt install -y python3-opencv
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv tiago_rtab_env
source tiago_rtab_env/bin/activate

# Install Python packages
pip install numpy opencv-python pyyaml matplotlib scipy transforms3d
```

### 2. Download and Setup

```bash
# Clone the workspace
git clone <repository-url> tiago_rtabmap_workspace
cd tiago_rtabmap_workspace

# Check environment
python tiago_rtabmap_slam/scripts/demo_setup.py check
```

### 3. Run Demo

```bash
# Start simulation demo
source tiago_rtab_env/bin/activate
python tiago_rtabmap_slam/scripts/demo_setup.py sim
```

## 📁 Project Structure

```
tiago_rtabmap_workspace/
├── tiago_rtabmap_slam/          # Main RTAB-Map package
│   ├── launch/                  # Launch files
│   │   ├── tiago_rtabmap_slam.launch.py      # Core SLAM launch
│   │   └── tiago_gazebo_rtabmap.launch.py    # Simulation launch
│   ├── config/                  # Configuration files
│   │   └── tiago_rtabmap.rviz   # RViz configuration
│   ├── scripts/                 # Utility scripts
│   │   ├── rtabmap_wrapper.py   # RTAB-Map control wrapper
│   │   └── demo_setup.py        # Demo setup script
│   ├── package.xml              # ROS 2 package definition
│   ├── CMakeLists.txt          # Build configuration
│   └── README.md               # Package documentation
├── tiago_gazebo/               # Existing TIAGo simulation
├── tiago_simulation/           # TIAGo simulation packages
├── tiago_rtab_env/            # Python virtual environment
└── SETUP_GUIDE.md             # This file
```

## 🔧 Configuration Options

### RTAB-Map Parameters

Key parameters in `launch/tiago_rtabmap_slam.launch.py`:

```python
# Basic SLAM settings
'Mem/IncrementalMemory': 'true'      # Enable incremental mapping
'RGBD/AngularUpdate': '0.1'          # Minimum rotation for new node (rad)
'RGBD/LinearUpdate': '0.1'           # Minimum translation for new node (m)

# Loop closure detection
'RGBD/NeighborLinkRefining': 'true'  # Refine odometry using visual features
'RGBD/ProximityBySpace': 'true'      # Use spatial proximity for loop closure

# 2D SLAM optimization
'Reg/Force3DoF': 'true'              # Force 3DoF (x, y, yaw) registration
'Optimizer/Slam2D': 'true'           # Use 2D graph optimization

# Grid mapping
'Grid/Sensor': '1'                   # Use both laser and RGB-D for mapping
'Grid/RayTracing': 'true'            # Enable ray tracing for free space
'Grid/RangeMax': '5.0'               # Maximum range for grid mapping
```

### Sensor Topics

The system expects these topics from TIAGo:

- **RGB Camera**: `/xtion/rgb/image_raw`
- **Depth Camera**: `/xtion/depth/image_raw`
- **Camera Info**: `/xtion/rgb/camera_info`, `/xtion/depth/camera_info`
- **Laser Scan**: `/scan_filtered`
- **Odometry**: `/mobile_base_controller/odom`

## 🎮 Usage Examples

### Basic Mapping

```bash
# 1. Start the system
source tiago_rtab_env/bin/activate
python tiago_rtabmap_slam/scripts/demo_setup.py sim

# 2. Control robot (in another terminal)
# Use keyboard controls: w=forward, s=backward, a=left, d=right

# 3. Monitor progress
# Watch the visualization windows for mapping progress
```

### Advanced Usage

```bash
# Custom database location
python launch/tiago_rtabmap_slam.launch.py database_path:=/path/to/map.db

# Localization mode (using existing map)
python launch/tiago_rtabmap_slam.launch.py localization:=true

# Headless operation (no GUI)
python launch/tiago_rtabmap_slam.launch.py launch_rviz:=false
```

### Real Robot Deployment

```bash
# 1. Connect to TIAGo robot network
ssh pal@<robot-ip>

# 2. Launch on robot
source tiago_rtab_env/bin/activate
python launch/tiago_rtabmap_slam.launch.py use_sim_time:=false

# 3. Monitor from development machine
rviz2 -d config/tiago_rtabmap.rviz
```

## 📊 Monitoring and Debugging

### Status Monitoring

The system provides real-time status through:

```bash
# Check RTAB-Map status
python -c "
import time
import yaml
# Monitor /rtabmap_status topic for detailed information
"

# View current map
rtabmap-databaseViewer ~/tiago_rtabmap.db

# Check topic connections
rostopic list | grep rtabmap
rostopic echo /rtabmap/info
```

### Performance Optimization

**For Real-time Performance:**
```python
# Reduce computational load
'Kp/MaxFeatures': '200'
'SURF/HessianThreshold': '200'
'RGBD/LinearUpdate': '0.2'
'RGBD/AngularUpdate': '0.2'
```

**For Map Quality:**
```python
# Increase features and accuracy
'Kp/MaxFeatures': '600'
'SURF/HessianThreshold': '100'
'RGBD/LinearUpdate': '0.05'
'RGBD/AngularUpdate': '0.05'
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Solution: Ensure virtual environment is activated
   source tiago_rtab_env/bin/activate
   pip install -r requirements.txt
   ```

2. **No Camera Data**
   ```bash
   # Check topic availability
   rostopic list | grep xtion
   rostopic hz /xtion/rgb/image_raw
   ```

3. **Poor Loop Closure**
   ```bash
   # Improve lighting, reduce speed, check parameters
   # Ensure sufficient visual features in environment
   ```

4. **High CPU Usage**
   ```bash
   # Reduce RTAB-Map feature extraction
   # Lower camera resolution
   # Increase update thresholds
   ```

### Debug Commands

```bash
# System diagnostics
htop                          # Monitor CPU/memory usage
nvidia-smi                    # Check GPU usage (if available)

# ROS diagnostics
ros2 topic list               # List all topics
ros2 node list               # List all nodes
ros2 service list            # List all services

# RTAB-Map specific
ros2 topic echo /rtabmap/info
ros2 service call /rtabmap/get_map rtabmap_ros/srv/GetMap
```

## 🔄 Integration with Navigation

To integrate with ROS 2 Navigation Stack:

```bash
# Install navigation packages
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-nav2-map-server

# Launch navigation with RTAB-Map
ros2 launch nav2_bringup navigation_launch.py \
    map:=/map \
    use_sim_time:=true
```

## 📈 Performance Benchmarks

Expected performance on different hardware:

| Hardware | FPS | CPU Usage | Memory | Notes |
|----------|-----|-----------|---------|-------|
| Laptop (i5, 8GB) | 5-10 | 60-80% | 2-4GB | Simulation |
| Desktop (i7, 16GB) | 10-15 | 40-60% | 3-6GB | Simulation |
| TIAGo Onboard | 3-8 | 70-90% | 1-3GB | Real robot |

## 🚢 Deployment Checklist

Before deploying on real robot:

- [ ] Test in simulation successfully
- [ ] Verify all sensors are working
- [ ] Check network connectivity
- [ ] Calibrate camera parameters
- [ ] Test emergency stop procedures
- [ ] Backup existing robot configuration

## 📚 Additional Resources

- [RTAB-Map Documentation](http://introlab.github.io/rtabmap/)
- [TIAGo Robot Manual](http://wiki.ros.org/Robots/TIAGo)
- [ROS 2 Navigation](https://navigation.ros.org/)
- [Computer Vision with OpenCV](https://opencv.org/)

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on the repository
- Join the ROS community forums
- Contact the maintainers

---

**Happy Mapping! 🗺️🤖**