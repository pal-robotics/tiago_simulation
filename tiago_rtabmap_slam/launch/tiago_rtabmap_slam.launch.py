#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def launch_setup(context, *args, **kwargs):
    """Setup launch based on configurations"""
    
    # Get package directories
    tiago_rtabmap_dir = get_package_share_directory('tiago_rtabmap_slam')
    
    # Launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    rtabmap_args = LaunchConfiguration('rtabmap_args')
    launch_rviz = LaunchConfiguration('launch_rviz')
    rviz_config = LaunchConfiguration('rviz_config')
    database_path = LaunchConfiguration('database_path')
    
    # RTAB-Map parameters
    rtabmap_parameters = {
        'use_sim_time': use_sim_time,
        'subscribe_depth': True,
        'subscribe_rgb': True,
        'subscribe_scan': True,
        'frame_id': 'base_footprint',
        'odom_frame_id': 'odom',
        'map_frame_id': 'map',
        'database_path': database_path,
        'approx_sync': True,
        'wait_for_transform': 0.2,
        'Mem/IncrementalMemory': 'true',
        'Mem/InitWMWithAllNodes': 'false',
        'RGBD/NeighborLinkRefining': 'true',
        'RGBD/ProximityBySpace': 'true',
        'RGBD/AngularUpdate': '0.1',
        'RGBD/LinearUpdate': '0.1',
        'Reg/Strategy': '0',
        'Reg/Force3DoF': 'true',
        'Grid/Sensor': '1',
        'Grid/3D': 'false',
        'Grid/RayTracing': 'true',
        'Grid/RangeMax': '5.0',
        'Grid/MaxObstacleHeight': '2.0',
        'Grid/NoiseFilteringRadius': '0.0',
        'Grid/NoiseFilteringMinNeighbors': '5',
        'Optimizer/Slam2D': 'true',
        'Optimizer/Strategy': '0',
        'SURF/HessianThreshold': '150',
    }
    
    # Convert rtabmap_args string to parameters
    rtabmap_args_str = rtabmap_args.perform(context)
    if rtabmap_args_str:
        for arg in rtabmap_args_str.split(','):
            if '=' in arg:
                key, value = arg.split('=', 1)
                rtabmap_parameters[key.strip()] = value.strip()

    # RTAB-Map node
    rtabmap_node = Node(
        package='rtabmap_ros',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        parameters=[rtabmap_parameters],
        remappings=[
            ('rgb/image', '/xtion/rgb/image_raw'),
            ('depth/image', '/xtion/depth/image_raw'),
            ('rgb/camera_info', '/xtion/rgb/camera_info'),
            ('depth/camera_info', '/xtion/depth/camera_info'),
            ('scan', '/scan_filtered'),
            ('odom', '/mobile_base_controller/odom'),
        ],
        arguments=[LaunchConfiguration('rtabmap_args')],
    )

    # RTAB-Map visualization node
    rtabmapviz_node = Node(
        package='rtabmap_ros',
        executable='rtabmapviz',
        name='rtabmapviz',
        output='screen',
        parameters=[rtabmap_parameters],
        remappings=[
            ('rgb/image', '/xtion/rgb/image_raw'),
            ('depth/image', '/xtion/depth/image_raw'),
            ('rgb/camera_info', '/xtion/rgb/camera_info'),
            ('depth/camera_info', '/xtion/depth/camera_info'),
            ('scan', '/scan_filtered'),
            ('odom', '/mobile_base_controller/odom'),
        ],
        condition=IfCondition(LaunchConfiguration('launch_rtabmapviz')),
    )

    # RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(launch_rviz),
    )

    # Point cloud to laser scan converter for TIAGo
    pointcloud_to_laserscan_node = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        parameters=[{
            'target_frame': 'base_laser_link',
            'transform_tolerance': 0.01,
            'min_height': -0.5,
            'max_height': 1.0,
            'angle_min': -1.5708,
            'angle_max': 1.5708,
            'angle_increment': 0.0087,
            'scan_time': 0.3333,
            'range_min': 0.45,
            'range_max': 8.0,
            'use_inf': True,
            'inf_epsilon': 1.0,
            'use_sim_time': use_sim_time,
        }],
        remappings=[
            ('cloud_in', '/xtion/depth_registered/points'),
            ('scan', '/scan_filtered'),
        ],
    )

    # Localization mode parameters
    localization_parameters = rtabmap_parameters.copy()
    localization_parameters.update({
        'Mem/IncrementalMemory': 'false',
        'Mem/InitWMWithAllNodes': 'true',
    })

    # RTAB-Map localization node (alternative mode)
    rtabmap_localization_node = Node(
        package='rtabmap_ros',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        parameters=[localization_parameters],
        remappings=[
            ('rgb/image', '/xtion/rgb/image_raw'),
            ('depth/image', '/xtion/depth/image_raw'),
            ('rgb/camera_info', '/xtion/rgb/camera_info'),
            ('depth/camera_info', '/xtion/depth/camera_info'),
            ('scan', '/scan_filtered'),
            ('odom', '/mobile_base_controller/odom'),
        ],
        condition=IfCondition(LaunchConfiguration('localization')),
    )

    return [
        rtabmap_node,
        rtabmapviz_node,
        rviz_node,
        pointcloud_to_laserscan_node,
    ]


def generate_launch_description():
    """Generate the launch description for TIAGo RTAB-Map SLAM"""
    
    # Get package directories
    tiago_rtabmap_dir = get_package_share_directory('tiago_rtabmap_slam')
    
    # Default RViz config path
    default_rviz_config = os.path.join(tiago_rtabmap_dir, 'config', 'tiago_rtabmap.rviz')
    
    # Default database path
    default_database_path = os.path.join(os.path.expanduser('~'), 'tiago_rtabmap.db')

    return LaunchDescription([
        # Launch arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time'
        ),
        DeclareLaunchArgument(
            'rtabmap_args',
            default_value='',
            description='Additional arguments for RTAB-Map'
        ),
        DeclareLaunchArgument(
            'launch_rviz',
            default_value='true',
            description='Launch RViz for visualization'
        ),
        DeclareLaunchArgument(
            'launch_rtabmapviz',
            default_value='false',
            description='Launch RTAB-Map visualization tool'
        ),
        DeclareLaunchArgument(
            'rviz_config',
            default_value=default_rviz_config,
            description='RViz configuration file'
        ),
        DeclareLaunchArgument(
            'database_path',
            default_value=default_database_path,
            description='Path to RTAB-Map database'
        ),
        DeclareLaunchArgument(
            'localization',
            default_value='false',
            description='Set to true for localization mode, false for mapping mode'
        ),
        
        # Launch setup
        OpaqueFunction(function=launch_setup),
    ])