^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package tiago_controller_configuration_gazebo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forthcoming
-----------
* Merge branch 'pid_for_suspension_caster' into 'erbium-devel'
  gains for suspension and caster joints
  See merge request robots/tiago_simulation!28
* pids for caster wheels
* gains for suspension and caster joints
* Contributors: Andrei Pasnicenco, Victor Lopez

0.0.18 (2018-03-21)
-------------------

0.0.17 (2018-02-20)
-------------------

0.0.16 (2018-02-16)
-------------------
* add fingertip force sensors
* Contributors: Jordi Pages

0.0.15 (2018-01-24)
-------------------
* use robot sufix in all launch files
* add PID for shunck gripper joint
* add files for schunk-gripper based tiago
* remove installation rule no longer needed
* remove files moved to pal_gripper
* Contributors: Jordi Pages

0.0.14 (2017-11-07)
-------------------

0.0.13 (2017-11-02)
-------------------
* fixed merge
* added support for tiago titanium chessboard
* Contributors: Hilario Tome

0.0.12 (2017-05-30)
-------------------

0.0.11 (2017-05-16)
-------------------
* Add camera parameter for Octomap with MoveIt!
* Add configurations for Tiago Iron
* Allow multiple Tiagos to use the navigation stack
* Contributors: AleDF, davidfernandez

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
