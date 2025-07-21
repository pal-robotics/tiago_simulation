#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    """Generate launch description for TIAGo with RTAB-Map SLAM"""
    
    # Package directories
    tiago_gazebo_dir = get_package_share_directory('tiago_gazebo')
    tiago_rtabmap_dir = get_package_share_directory('tiago_rtabmap_slam')
    
    # Launch arguments
    world_name = LaunchConfiguration('world_name')
    robot_name = LaunchConfiguration('robot_name')
    gui = LaunchConfiguration('gui')
    debug = LaunchConfiguration('debug')
    recording = LaunchConfiguration('recording')
    use_sim_time = LaunchConfiguration('use_sim_time')
    launch_rviz = LaunchConfiguration('launch_rviz')
    database_path = LaunchConfiguration('database_path')
    
    # Default paths
    default_world = os.path.join(tiago_gazebo_dir, 'worlds', 'small_office.world')
    default_rviz_config = os.path.join(tiago_rtabmap_dir, 'config', 'tiago_rtabmap.rviz')
    default_database = os.path.join(os.path.expanduser('~'), 'tiago_rtabmap.db')

    # TIAGo Gazebo simulation
    tiago_gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('tiago_gazebo'),
                'launch',
                'tiago_gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'world_name': world_name,
            'robot_name': robot_name,
            'gui': gui,
            'debug': debug,
            'recording': recording,
        }.items()
    )

    # RTAB-Map SLAM (delayed start to allow simulation to initialize)
    rtabmap_slam_launch = TimerAction(
        period=5.0,  # Wait 5 seconds for simulation to start
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        FindPackageShare('tiago_rtabmap_slam'),
                        'launch',
                        'tiago_rtabmap_slam.launch.py'
                    ])
                ]),
                launch_arguments={
                    'use_sim_time': use_sim_time,
                    'launch_rviz': launch_rviz,
                    'database_path': database_path,
                }.items()
            )
        ]
    )

    # Static transform publishers for camera frame corrections
    static_tf_xtion_optical = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher_xtion_optical',
        arguments=[
            '0', '0', '0',
            '-1.5708', '0', '-1.5708',
            'xtion_rgb_frame', 'xtion_rgb_optical_frame'
        ],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    static_tf_xtion_depth_optical = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher_xtion_depth_optical',
        arguments=[
            '0', '0', '0',
            '-1.5708', '0', '-1.5708',
            'xtion_depth_frame', 'xtion_depth_optical_frame'
        ],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Laser filter to clean up laser scan data
    laser_filter_node = Node(
        package='laser_filters',
        executable='scan_to_scan_filter_chain',
        name='laser_filter',
        parameters=[{
            'use_sim_time': use_sim_time,
            'scan_filter_chain': [
                {
                    'name': 'range_filter',
                    'type': 'laser_filters/LaserScanRangeFilter',
                    'params': {
                        'use_message_stamp_for_transform': False,
                        'lower_threshold': 0.1,
                        'upper_threshold': 8.0,
                        'lower_replacement_value': float('nan'),
                        'upper_replacement_value': float('nan'),
                    }
                },
                {
                    'name': 'angular_bounds_filter',
                    'type': 'laser_filters/LaserScanAngularBoundsFilter',
                    'params': {
                        'use_message_stamp_for_transform': False,
                        'lower_angle': -1.5708,
                        'upper_angle': 1.5708,
                    }
                }
            ]
        }],
        remappings=[
            ('scan', '/scan_raw'),
            ('scan_filtered', '/scan_filtered'),
        ]
    )

    return LaunchDescription([
        # Launch arguments
        DeclareLaunchArgument(
            'world_name',
            default_value=default_world,
            description='World file for Gazebo'
        ),
        DeclareLaunchArgument(
            'robot_name',
            default_value='tiago',
            description='Robot name'
        ),
        DeclareLaunchArgument(
            'gui',
            default_value='true',
            description='Launch Gazebo GUI'
        ),
        DeclareLaunchArgument(
            'debug',
            default_value='false',
            description='Enable debug mode'
        ),
        DeclareLaunchArgument(
            'recording',
            default_value='false',
            description='Enable recording'
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time'
        ),
        DeclareLaunchArgument(
            'launch_rviz',
            default_value='true',
            description='Launch RViz for visualization'
        ),
        DeclareLaunchArgument(
            'database_path',
            default_value=default_database,
            description='Path to RTAB-Map database'
        ),

        # Launch nodes
        tiago_gazebo_launch,
        rtabmap_slam_launch,
        static_tf_xtion_optical,
        static_tf_xtion_depth_optical,
        laser_filter_node,
    ])