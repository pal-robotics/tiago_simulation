^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package tiago_gazebo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
