#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from std_msgs.msg import String, Bool
from std_srvs.srv import Empty
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import Image, CompressedImage, LaserScan
from cv_bridge import CvBridge
import cv2
import os
import yaml
import subprocess
import threading
import time


class TIAGoRTABMapWrapper(Node):
    """
    TIAGo RTAB-Map Wrapper Node
    
    This node provides high-level control and monitoring for RTAB-Map SLAM
    operations with TIAGo robot, including:
    - Map saving and loading
    - Switching between mapping and localization modes
    - Data collection monitoring
    - Real-time status reporting
    """
    
    def __init__(self):
        super().__init__('tiago_rtabmap_wrapper')
        
        # Initialize CvBridge for image processing
        self.cv_bridge = CvBridge()
        
        # Configuration parameters
        self.declare_parameter('database_path', '~/tiago_rtabmap.db')
        self.declare_parameter('maps_directory', '~/tiago_maps/')
        self.declare_parameter('auto_save_interval', 60.0)  # seconds
        self.declare_parameter('use_sim_time', True)
        
        self.database_path = self.get_parameter('database_path').value
        self.maps_directory = self.get_parameter('maps_directory').value
        self.auto_save_interval = self.get_parameter('auto_save_interval').value
        
        # Ensure directories exist
        os.makedirs(os.path.expanduser(self.maps_directory), exist_ok=True)
        
        # QoS profiles
        qos_reliable = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        qos_best_effort = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # Publishers
        self.status_pub = self.create_publisher(String, 'rtabmap_status', qos_reliable)
        self.cmd_vel_pub = self.create_publisher(Twist, '/mobile_base_controller/cmd_vel', qos_reliable)
        
        # Subscribers
        self.map_sub = self.create_subscription(
            OccupancyGrid, '/map', self.map_callback, qos_reliable)
        self.image_sub = self.create_subscription(
            Image, '/xtion/rgb/image_raw', self.image_callback, qos_best_effort)
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan_filtered', self.scan_callback, qos_best_effort)
        
        # Service clients
        self.reset_client = self.create_client(Empty, '/rtabmap/reset')
        self.pause_client = self.create_client(Empty, '/rtabmap/pause')
        self.resume_client = self.create_client(Empty, '/rtabmap/resume')
        
        # Status variables
        self.mapping_active = True
        self.last_map_time = None
        self.last_image_time = None
        self.last_scan_time = None
        self.nodes_count = 0
        self.loop_closures = 0
        
        # Auto-save timer
        self.auto_save_timer = self.create_timer(
            self.auto_save_interval, self.auto_save_callback)
        
        # Status publishing timer
        self.status_timer = self.create_timer(1.0, self.publish_status)
        
        self.get_logger().info('TIAGo RTAB-Map Wrapper initialized')
        
    def map_callback(self, msg):
        """Handle map updates"""
        self.last_map_time = self.get_clock().now()
        # Process map data if needed
        
    def image_callback(self, msg):
        """Handle RGB image updates"""
        self.last_image_time = self.get_clock().now()
        # Can process images for visual features if needed
        
    def scan_callback(self, msg):
        """Handle laser scan updates"""
        self.last_scan_time = self.get_clock().now()
        # Process scan data if needed
        
    def publish_status(self):
        """Publish current RTAB-Map status"""
        status_msg = String()
        current_time = self.get_clock().now()
        
        status_data = {
            'mapping_active': self.mapping_active,
            'nodes_count': self.nodes_count,
            'loop_closures': self.loop_closures,
            'last_map_update': self.time_since(self.last_map_time),
            'last_image_update': self.time_since(self.last_image_time),
            'last_scan_update': self.time_since(self.last_scan_time),
            'database_path': self.database_path
        }
        
        status_msg.data = yaml.dump(status_data)
        self.status_pub.publish(status_msg)
        
    def time_since(self, timestamp):
        """Calculate time since given timestamp"""
        if timestamp is None:
            return None
        current_time = self.get_clock().now()
        return (current_time - timestamp).nanoseconds / 1e9
        
    def auto_save_callback(self):
        """Auto-save map periodically"""
        if self.mapping_active:
            self.save_map(auto=True)
            
    def save_map(self, filename=None, auto=False):
        """Save current map to file"""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            prefix = "auto_" if auto else "manual_"
            filename = f"{prefix}tiago_map_{timestamp}"
            
        map_path = os.path.join(
            os.path.expanduser(self.maps_directory), 
            filename
        )
        
        try:
            # Save map using map_server
            cmd = [
                'ros2', 'run', 'nav2_map_server', 'map_saver_cli',
                '-f', map_path,
                '--ros-args', '-p', 'use_sim_time:=true'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if not auto:
                    self.get_logger().info(f'Map saved successfully: {map_path}')
            else:
                self.get_logger().error(f'Failed to save map: {result.stderr}')
                
        except Exception as e:
            self.get_logger().error(f'Error saving map: {str(e)}')
            
    def reset_rtabmap(self):
        """Reset RTAB-Map database"""
        if not self.reset_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('Reset service not available')
            return False
            
        try:
            request = Empty.Request()
            future = self.reset_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            
            if future.result() is not None:
                self.get_logger().info('RTAB-Map reset successfully')
                return True
            else:
                self.get_logger().error('Failed to reset RTAB-Map')
                return False
                
        except Exception as e:
            self.get_logger().error(f'Error resetting RTAB-Map: {str(e)}')
            return False
            
    def pause_mapping(self):
        """Pause RTAB-Map mapping"""
        if not self.pause_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('Pause service not available')
            return False
            
        try:
            request = Empty.Request()
            future = self.pause_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            
            if future.result() is not None:
                self.mapping_active = False
                self.get_logger().info('RTAB-Map mapping paused')
                return True
            else:
                self.get_logger().error('Failed to pause RTAB-Map')
                return False
                
        except Exception as e:
            self.get_logger().error(f'Error pausing RTAB-Map: {str(e)}')
            return False
            
    def resume_mapping(self):
        """Resume RTAB-Map mapping"""
        if not self.resume_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('Resume service not available')
            return False
            
        try:
            request = Empty.Request()
            future = self.resume_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            
            if future.result() is not None:
                self.mapping_active = True
                self.get_logger().info('RTAB-Map mapping resumed')
                return True
            else:
                self.get_logger().error('Failed to resume RTAB-Map')
                return False
                
        except Exception as e:
            self.get_logger().error(f'Error resuming RTAB-Map: {str(e)}')
            return False
            
    def emergency_stop(self):
        """Emergency stop robot movement"""
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        
        for _ in range(10):  # Send multiple stop commands
            self.cmd_vel_pub.publish(stop_msg)
            time.sleep(0.1)
            
        self.get_logger().warn('Emergency stop executed')


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = TIAGoRTABMapWrapper()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if 'node' in locals():
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()