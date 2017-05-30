^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package tiago_gazebo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forthcoming
-----------
* Add sun and ground_plane models
* Contributors: Victor Lopez

0.0.11 (2017-05-16)
-------------------
* Add camera parameter for Octomap with MoveIt!
* Allow multiple Tiagos to use the navigation stack
* Allow multiple Tiagos on Gazebo
  Fixes #15402
* Fix z height from Gazebo world objects_on_table
* Add lights in front of the people to fix color
  Given that Gazebo renders the models of the people very dark as can be seen in the TIAGo tutorial:
  ![TIAGo tutorial people rendered dark screenshot](http://wiki.ros.org/Robots/TIAGo/Tutorials/PersonDetection?action=AttachFile&do=get&target=gazebo_person_detection.jpg)
  I added some lights in front of the models so they become more visible.
* add Willow Garage world
* Contributors: Adria Roig, AleDF, David Fernandez, Jordi Pages, Sam Pfeiffer, davidfernandez

0.0.10 (2016-10-21)
-------------------

0.0.9 (2016-10-14)
------------------
* add aruco board
* move a bit farther the pringles can
* add a poster in the tutorial office for opencv_tut
* refs #14222. Do not call simple_action_grasping
  In public simulation this package is unreleased
* Add simulation world and model for refs #14521
* add look_to_point example world and models
* use proper pal_hardware_gazebo yaml file
* add sonars and depth image
* fix tiago_controller_configuration_gazebo dep
* set myself as maintainer
* launch files to support public map/loc
* add export to remove some error prints
* convert to rectangular box and fix inertia
* fix sdf version
* change slightly the pose of the table and cube
* add 5 cm single marker side cube
* disable dynamic_footprint when public_sim=true
* add missing running dependencies
* set up simulation for Steel and Titanium versions
* set steel robot for grasping demo
* New worlds for Apps/tiago_tutorials
* add simulation world and models
* New launch file for the pick and place demo, also provided the world
* improve inertia, friction and collision model
* remove home motion to speed up demo
* grasping demo using green cube
* add separate motions file and fix can intertia
* Add a image_rect_color topic republishing image_raw rgb image to have the same interface in simulation
* Added aruco cube and world
* Contributors: Jordi Pages, Sam Pfeiffer, job-1994

0.0.7 (2016-06-15)
------------------

0.0.6 (2016-06-15)
------------------
* add missing launch sonar_to_cloud
* Contributors: Jeremie Deray

0.0.5 (2016-06-15)
------------------
* Change default robot to custom for some launch files
* Contributors: Victor Lopez

0.0.4 (2016-06-15)
------------------

0.0.3 (2016-06-14)
------------------
* Updated simulation for imu and force torque
* Add simulation controller configuration package
  Also make the simulation launch that related controllers instead of the tiago_bringup ones
* Update package.xml to pull pal_hardware_gazebo dependence
* Cleanup
* Make steel default
* Added navigation visualisation to rviz
* Contributors: Bence Magyar, Jordi Adell, Sam Pfeiffer

0.0.2 (2015-04-15)
------------------

0.0.1 (2015-04-15)
------------------
* Install tuck script and configuration files
* Add tuck_arm to gazebo launch sequence
* Robot spawns on the ground instead of tiny elevation
* Pass robot param to bringup
* Changed default value of robot to titanium
* add camera view in rviz and modify objects places
* Fix conflict...
* Add objects on table world and belongings
  Conflicts:
  tiago_gazebo/worlds/objects_on_table.world
* add tiago standalone rviz configuration file
* add simulated worlds
* add rviz for whole body control testing
* refs #10237 : adds small_office world
* Lower spawn height
* Initial commit of tiago_simulation
* Contributors: Bence Magyar, Jordi Pages, enriquefernandez
