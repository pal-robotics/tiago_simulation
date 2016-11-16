^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package tiago_controller_configuration_gazebo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.0.10 (2016-10-21)
-------------------
* Fixed bug in yaml parameters. Added imu_sensor for all the configurations
* Contributors: Adria Roig

0.0.9 (2016-10-14)
------------------
* Updated imu parameter tiago pal hardware gazebo
* refs #14222. Do not call simple_action_grasping
  In public simulation this package is unreleased
* use proper pal_hardware_gazebo yaml file
* set myself as maintainer
* set up simulation for Steel and Titanium versions
* add xml tag to show colours in gedit
* fix error in gripper controller joints names
* Contributors: Hilario Tome, Jordi Pages

0.0.8 (2016-07-08)
------------------
* tell play_motion which robot is running
  possible args: custom, steel or titanium
* Contributors: Jordi Pages

0.0.7 (2016-06-15)
------------------

0.0.6 (2016-06-15)
------------------

0.0.5 (2016-06-15)
------------------

0.0.4 (2016-06-15)
------------------
* Fix name of imu_controller launch
* Contributors: Victor Lopez

0.0.3 (2016-06-14)
------------------
* fix version number
* Added play motion to controllers startup in simulation
* Updated simulation for imu and force torque
* Add simulation controller configuration package
  Also make the simulation launch that related controllers instead of the tiago_bringup ones
* Contributors: Sam Pfeiffer, jordi.pages@pal-robotics.com
