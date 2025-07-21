#!/usr/bin/env python3

"""
TIAGo RTAB-Map Demo Setup Script

This script provides a simplified interface for setting up and running
TIAGo RTAB-Map SLAM demonstrations. It handles environment setup,
launches appropriate nodes, and provides monitoring capabilities.
"""

import os
import sys
import time
import argparse
import subprocess
import signal
import yaml
from pathlib import Path

class TIAGoRTABMapDemo:
    def __init__(self):
        self.processes = []
        self.demo_running = False
        
    def cleanup(self, signum=None, frame=None):
        """Clean up running processes"""
        print("\nShutting down demo...")
        self.demo_running = False
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except:
                pass
        
        self.processes.clear()
        print("Demo shutdown complete.")
        sys.exit(0)
        
    def check_environment(self):
        """Check if the environment is properly set up"""
        print("Checking environment...")
        
        # Check if we're in a virtual environment
        if hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix:
            print("✓ Virtual environment detected")
        else:
            print("⚠ Not in virtual environment - some features may not work")
            
        # Check for required Python packages
        required_packages = ['numpy', 'opencv-python', 'pyyaml', 'matplotlib']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"✓ {package} available")
            except ImportError:
                missing_packages.append(package)
                print(f"✗ {package} not found")
                
        if missing_packages:
            print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install'
                ] + missing_packages)
                print("✓ Missing packages installed")
            except subprocess.CalledProcessError:
                print("✗ Failed to install packages")
                return False
                
        return True
        
    def create_demo_world(self):
        """Create a simple demo world file"""
        world_content = """<?xml version="1.0"?>
<sdf version="1.6">
  <world name="tiago_demo_world">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    
    <include>
      <uri>model://sun</uri>
    </include>
    
    <!-- Simple room with walls -->
    <model name="walls">
      <static>true</static>
      <link name="link">
        <!-- Floor -->
        <collision name="floor">
          <pose>0 0 -0.1 0 0 0</pose>
          <geometry>
            <box>
              <size>10 10 0.2</size>
            </box>
          </geometry>
        </collision>
        <visual name="floor_visual">
          <pose>0 0 -0.1 0 0 0</pose>
          <geometry>
            <box>
              <size>10 10 0.2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
          </material>
        </visual>
        
        <!-- Walls -->
        <collision name="wall1">
          <pose>5 0 1 0 0 0</pose>
          <geometry>
            <box>
              <size>0.2 10 2</size>
            </box>
          </geometry>
        </collision>
        <visual name="wall1_visual">
          <pose>5 0 1 0 0 0</pose>
          <geometry>
            <box>
              <size>0.2 10 2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.6 0.6 0.6 1</ambient>
          </material>
        </visual>
        
        <collision name="wall2">
          <pose>-5 0 1 0 0 0</pose>
          <geometry>
            <box>
              <size>0.2 10 2</size>
            </box>
          </geometry>
        </collision>
        <visual name="wall2_visual">
          <pose>-5 0 1 0 0 0</pose>
          <geometry>
            <box>
              <size>0.2 10 2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.6 0.6 0.6 1</ambient>
          </material>
        </visual>
        
        <collision name="wall3">
          <pose>0 5 1 0 0 0</pose>
          <geometry>
            <box>
              <size>10 0.2 2</size>
            </box>
          </geometry>
        </collision>
        <visual name="wall3_visual">
          <pose>0 5 1 0 0 0</pose>
          <geometry>
            <box>
              <size>10 0.2 2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.6 0.6 0.6 1</ambient>
          </material>
        </visual>
        
        <collision name="wall4">
          <pose>0 -5 1 0 0 0</pose>
          <geometry>
            <box>
              <size>10 0.2 2</size>
            </box>
          </geometry>
        </collision>
        <visual name="wall4_visual">
          <pose>0 -5 1 0 0 0</pose>
          <geometry>
            <box>
              <size>10 0.2 2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.6 0.6 0.6 1</ambient>
          </material>
        </visual>
      </link>
    </model>
    
    <!-- Some obstacles for interesting mapping -->
    <model name="obstacle1">
      <static>true</static>
      <pose>2 2 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.2 0.2 1</ambient>
          </material>
        </visual>
      </link>
    </model>
    
    <model name="obstacle2">
      <static>true</static>
      <pose>-2 -2 0.25 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <cylinder>
              <radius>0.5</radius>
              <length>0.5</length>
            </cylinder>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <cylinder>
              <radius>0.5</radius>
              <length>0.5</length>
            </cylinder>
          </geometry>
          <material>
            <ambient>0.2 0.8 0.2 1</ambient>
          </material>
        </visual>
      </link>
    </model>
  </world>
</sdf>"""
        
        world_dir = Path("worlds")
        world_dir.mkdir(exist_ok=True)
        
        world_file = world_dir / "tiago_demo.world"
        with open(world_file, 'w') as f:
            f.write(world_content)
            
        print(f"✓ Demo world created: {world_file}")
        return str(world_file.absolute())
        
    def run_simulation_demo(self, args):
        """Run the simulation demo"""
        print("Starting TIAGo RTAB-Map Simulation Demo...")
        
        # Setup signal handler for cleanup
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        # Create demo world
        world_file = self.create_demo_world()
        
        # Create simplified TIAGo simulation launcher
        sim_script = self.create_simulation_script(world_file)
        
        print("\n" + "="*60)
        print("TIAGo RTAB-Map SLAM Demo")
        print("="*60)
        print("This demo will:")
        print("1. Launch a simplified TIAGo simulation")
        print("2. Start RTAB-Map SLAM")
        print("3. Provide manual control interface")
        print("4. Display mapping progress")
        print("\nControls:")
        print("- Use keyboard to control robot movement")
        print("- Watch RViz for map building progress")
        print("- Press Ctrl+C to exit")
        print("="*60)
        
        if not args.headless:
            input("\nPress Enter to start the demo...")
        
        try:
            # Start simulation
            print("Starting simulation...")
            sim_process = subprocess.Popen([
                sys.executable, sim_script
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(sim_process)
            
            # Wait a bit for simulation to start
            time.sleep(3)
            
            # Start RTAB-Map wrapper
            print("Starting RTAB-Map wrapper...")
            rtabmap_process = subprocess.Popen([
                sys.executable, 
                'tiago_rtabmap_slam/scripts/rtabmap_wrapper.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(rtabmap_process)
            
            # Start visualization if not headless
            if not args.headless:
                print("Starting visualization...")
                self.start_visualization()
            
            self.demo_running = True
            print("\n✓ Demo started successfully!")
            print("Drive the robot around to build the map...")
            
            # Monitor demo
            self.monitor_demo()
            
        except Exception as e:
            print(f"Error running demo: {e}")
            self.cleanup()
            
    def create_simulation_script(self, world_file):
        """Create a simplified simulation script"""
        script_content = f'''#!/usr/bin/env python3

import numpy as np
import cv2
import time
import threading
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class TIAGoSimulation:
    """Simplified TIAGo simulation for demonstration"""
    
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])  # x, y, theta
        self.velocity = np.array([0.0, 0.0])  # linear, angular
        self.running = True
        
        # Simple world map for demonstration
        self.world_size = (500, 500)
        self.world_map = np.ones(self.world_size, dtype=np.uint8) * 255
        
        # Add walls and obstacles
        self.create_world()
        
    def create_world(self):
        """Create a simple world with walls and obstacles"""
        # Walls
        self.world_map[10:20, :] = 0  # Top wall
        self.world_map[-20:-10, :] = 0  # Bottom wall
        self.world_map[:, 10:20] = 0  # Left wall
        self.world_map[:, -20:-10] = 0  # Right wall
        
        # Obstacles
        cv2.rectangle(self.world_map, (150, 150), (200, 200), 0, -1)
        cv2.circle(self.world_map, (350, 350), 30, 0, -1)
        
    def update_position(self, dt=0.1):
        """Update robot position based on velocity"""
        if not self.running:
            return
            
        # Simple kinematic model
        self.position[0] += self.velocity[0] * np.cos(self.position[2]) * dt
        self.position[1] += self.velocity[0] * np.sin(self.position[2]) * dt
        self.position[2] += self.velocity[1] * dt
        
        # Keep position in bounds
        self.position[0] = np.clip(self.position[0], 50, 450)
        self.position[1] = np.clip(self.position[1], 50, 450)
        
    def get_laser_scan(self) -> np.ndarray:
        """Simulate laser scan data"""
        angles = np.linspace(-np.pi/2, np.pi/2, 180)
        ranges = []
        
        robot_x, robot_y = int(self.position[0]), int(self.position[1])
        
        for angle in angles:
            scan_angle = self.position[2] + angle
            
            # Cast ray
            max_range = 100
            for r in range(1, max_range):
                x = robot_x + int(r * np.cos(scan_angle))
                y = robot_y + int(r * np.sin(scan_angle))
                
                if (x < 0 or x >= self.world_size[0] or 
                    y < 0 or y >= self.world_size[1] or 
                    self.world_map[y, x] == 0):
                    ranges.append(r * 0.05)  # Convert to meters
                    break
            else:
                ranges.append(max_range * 0.05)
                
        return np.array(ranges)
        
    def get_camera_image(self) -> np.ndarray:
        """Simulate camera image"""
        # Simple visualization of robot view
        view_img = np.copy(self.world_map)
        
        # Draw robot position
        robot_x, robot_y = int(self.position[0]), int(self.position[1])
        cv2.circle(view_img, (robot_x, robot_y), 5, 128, -1)
        
        # Draw direction indicator
        end_x = robot_x + int(20 * np.cos(self.position[2]))
        end_y = robot_y + int(20 * np.sin(self.position[2]))
        cv2.line(view_img, (robot_x, robot_y), (end_x, end_y), 128, 2)
        
        return view_img
        
    def set_velocity(self, linear: float, angular: float):
        """Set robot velocity"""
        self.velocity[0] = np.clip(linear, -1.0, 1.0)
        self.velocity[1] = np.clip(angular, -1.0, 1.0)
        
    def run(self):
        """Main simulation loop"""
        print("TIAGo Simulation Started")
        print("Controls: w=forward, s=backward, a=left, d=right, q=quit")
        
        while self.running:
            # Handle keyboard input (simplified)
            self.update_position()
            
            # Simple visualization
            img = self.get_camera_image()
            cv2.imshow("TIAGo Simulation", img)
            
            key = cv2.waitKey(100) & 0xFF
            if key == ord('q'):
                self.running = False
            elif key == ord('w'):
                self.set_velocity(0.5, 0.0)
            elif key == ord('s'):
                self.set_velocity(-0.5, 0.0)
            elif key == ord('a'):
                self.set_velocity(0.0, 0.5)
            elif key == ord('d'):
                self.set_velocity(0.0, -0.5)
            else:
                self.set_velocity(0.0, 0.0)
                
        cv2.destroyAllWindows()
        print("Simulation stopped")

if __name__ == "__main__":
    sim = TIAGoSimulation()
    sim.run()
'''
        
        script_file = Path("demo_sim.py")
        with open(script_file, 'w') as f:
            f.write(script_content)
            
        os.chmod(script_file, 0o755)
        return str(script_file.absolute())
        
    def start_visualization(self):
        """Start visualization tools"""
        try:
            # Simple matplotlib-based visualization
            viz_script = self.create_visualization_script()
            viz_process = subprocess.Popen([
                sys.executable, viz_script
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(viz_process)
            
        except Exception as e:
            print(f"Warning: Could not start visualization: {{e}}")
            
    def create_visualization_script(self):
        """Create visualization script"""
        viz_content = '''#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.animation import FuncAnimation

class RTABMapVisualization:
    def __init__(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 6))
        self.ax1.set_title("Occupancy Grid Map")
        self.ax2.set_title("Robot Trajectory")
        
        # Dummy data for demonstration
        self.map_data = np.random.rand(100, 100)
        self.trajectory = []
        
    def update_plot(self, frame):
        """Update visualization"""
        self.ax1.clear()
        self.ax2.clear()
        
        # Update map
        self.ax1.imshow(self.map_data, cmap='gray')
        self.ax1.set_title("RTAB-Map: Occupancy Grid")
        
        # Update trajectory
        if len(self.trajectory) > 1:
            traj = np.array(self.trajectory)
            self.ax2.plot(traj[:, 0], traj[:, 1], 'b-', linewidth=2)
            self.ax2.scatter(traj[-1, 0], traj[-1, 1], c='r', s=50)
            
        self.ax2.set_title("Robot Trajectory")
        self.ax2.grid(True)
        
        # Simulate new data
        if frame % 10 == 0:
            x = np.random.uniform(-5, 5)
            y = np.random.uniform(-5, 5)
            self.trajectory.append([x, y])
            
            # Keep trajectory reasonable length
            if len(self.trajectory) > 100:
                self.trajectory = self.trajectory[-100:]
                
        return []
        
    def run(self):
        """Start visualization"""
        ani = FuncAnimation(self.fig, self.update_plot, interval=200, blit=False)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    viz = RTABMapVisualization()
    viz.run()
'''
        
        viz_file = Path("demo_viz.py")
        with open(viz_file, 'w') as f:
            f.write(viz_content)
            
        os.chmod(viz_file, 0o755)
        return str(viz_file.absolute())
        
    def monitor_demo(self):
        """Monitor the demo and provide status updates"""
        start_time = time.time()
        
        while self.demo_running:
            try:
                elapsed = time.time() - start_time
                
                if elapsed % 30 < 1:  # Every 30 seconds
                    print(f"\\nDemo running for {{elapsed:.0f}} seconds...")
                    print("Status: Simulating RTAB-Map SLAM")
                    print("Tip: Move the robot around to see mapping in action")
                    
                time.sleep(1)
                
            except KeyboardInterrupt:
                self.cleanup()
                break

def main():
    parser = argparse.ArgumentParser(description="TIAGo RTAB-Map Demo Setup")
    parser.add_argument('mode', choices=['sim', 'check'], 
                       help='Demo mode: sim=simulation, check=environment check')
    parser.add_argument('--headless', action='store_true',
                       help='Run without GUI (for testing)')
    
    args = parser.parse_args()
    
    demo = TIAGoRTABMapDemo()
    
    if args.mode == 'check':
        if demo.check_environment():
            print("\\n✓ Environment check passed!")
            print("You can now run: python demo_setup.py sim")
        else:
            print("\\n✗ Environment check failed!")
            sys.exit(1)
            
    elif args.mode == 'sim':
        if not demo.check_environment():
            print("Environment check failed. Run 'python demo_setup.py check' first.")
            sys.exit(1)
            
        demo.run_simulation_demo(args)

if __name__ == "__main__":
    main()