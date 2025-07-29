from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    qos = LaunchConfiguration('qos')
    localization = LaunchConfiguration('localization')
    
    # --- Change this if Tiago's base frame is not base_footprint ---
    base_frame = 'base_footprint'  # or 'base_link', check your TF tree!

    parameters = {
        'frame_id': base_frame,
        'use_sim_time': use_sim_time,
        'subscribe_depth': True,                # 3D mapping ON
        'subscribe_rgb': True,                  # 3D mapping ON
        'subscribe_scan': True,                 # Use laser/LiDAR
        'subscribe_scan_cloud':True,
        'approx_sync': True,
        'use_action_for_goal': True,
        'qos_scan': qos,
        'qos_imu': qos,
        'Reg/Strategy': '1',
        'Reg/Force3DoF': 'true',
        'RGBD/NeighborLinkRefining': 'True',
        'Grid/RangeMin': '0.2',
        'Optimizer/GravitySigma': '0'
    }

    # Remap RTAB-Map's expected camera topics to Tiago's actual topics
    remappings = [
        # RGB camera
        ('rgb/image', '/head_front_camera/rgb/image_raw'),
        ('rgb/camera_info', '/head_front_camera/rgb/camera_info'),
        # Depth
        ('depth/image', '/head_front_camera/depth/image_raw'),
        ('depth/camera_info', '/head_front_camera/depth/camera_info'),
        # PointCloud (for colored voxels)
        ('rgbd_image', '/head_front_camera/rgbd/image'),
        ('depth/points', '/head_front_camera/depth/points'),
        # LIDAR
        ('scan', '/scan_raw'),
        ('odom', '/mobile_base_controller/odom'),
    ]

    # You may want to make your own RViz config later!
    rviz_config_dir = os.path.join(
        get_package_share_directory('rtabmap_ros'),
        'launch',  # or 'rviz'
        'rtabmap.rviz'   # Replace with your RViz config or make a new one
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument(
            'qos', default_value='2',
            description='QoS used for input sensor topics'),
        DeclareLaunchArgument(
            'localization', default_value='false',
            description='Launch in localization mode.'),

        # SLAM mode
        Node(
            condition=UnlessCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters],
            remappings=remappings,
            arguments=['-d']
        ),
        # Localization mode
        Node(
            condition=IfCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters, {
                'Mem/IncrementalMemory': 'False',
                'Mem/InitWMWithAllNodes': 'True'
            }],
            remappings=remappings,
        ),
        # RTAB-Map visualization
        Node(
            package='rtabmap_viz', executable='rtabmap_viz', output='screen',
            parameters=[parameters],
            remappings=remappings
        ),
        # RViz2
        Node(
            package='rviz2', executable='rviz2', output='screen',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}]
        ),
    ])