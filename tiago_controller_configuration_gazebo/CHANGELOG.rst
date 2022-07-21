^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package tiago_controller_configuration_gazebo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.3.3 (2022-07-21)
------------------
* Merge branch 'add_omni_tiago' into 'erbium-devel'
  Add base_type to the missing launch files
  See merge request robots/tiago_simulation!84
* Add base_type to the parameters for the motion choice
* =Add base_type to the missing launch files
* Contributors: saikishor, thomaspeyrucain

2.3.2 (2022-07-19)
------------------

2.3.1 (2022-05-11)
------------------

2.3.0 (2022-05-03)
------------------
* Merge branch 'no-end-effector-bugfix' into 'erbium-devel'
  No end effector bugfix
  See merge request robots/tiago_simulation!82
* fix pid with param override
* Add pid configuration for no end-effector
* update eval function and generate config files
* fix pid with param override
* Add pid configuration for no end-effector
* update eval function and generate config files
* Contributors: David ter Kuile, saikishor

2.2.6 (2022-03-21)
------------------
* Merge branch 'add_robotiq_epick_gripper' into 'erbium-devel'
  Add config files for epick gripper on Gazebo
  See merge request robots/tiago_simulation!81
* Add config files for epick gripper on Gazebo
* Contributors: saikishor, thomaspeyrucain

2.2.5 (2022-02-23)
------------------

2.2.4 (2022-01-04)
------------------

2.2.3 (2021-11-25)
------------------
* Merge branch 'fix-omni-base' into 'erbium-devel'
  Removed duplicated pid file
  See merge request robots/tiago_simulation!79
* adapting to the new omni drive controlle rfilters
* removing the needs for two pids files
* Contributors: antoniobrandi, saikishor

2.2.2 (2021-11-18)
------------------

2.2.1 (2021-11-09)
------------------

2.2.0 (2021-11-03)
------------------
* Merge branch 'omni_base_robot' into 'erbium-devel'
  Omni base robot
  See merge request robots/tiago_simulation!75
* tiago navigation with omni base
* omni base robot
* Contributors: antoniobrandi, saikishor

2.1.1 (2021-09-28)
------------------

2.1.0 (2021-05-06)
------------------
* Merge branch 'robotiq_gripper' into 'erbium-devel'
  Robotiq gripper
  See merge request robots/tiago_simulation!72
* added missing pal_robotiq_controller_configuration_gazebo dependency
* added robotiq gripper configuration
* Update pal hardware gazebo files for the robotiq grippers
* Contributors: Sai Kishor Kothakota, saikishor

2.0.23 (2020-07-30)
-------------------
* Merge branch 'rename_tf_prefix' into 'erbium-devel'
  Rename tf_prefix to robot_namespace
  See merge request robots/tiago_simulation!70
* Rename tf_prefix to robot_namespace
* Contributors: davidfernandez, victor

2.0.22 (2020-04-21)
-------------------
* Merge branch 'custom-ee' into 'erbium-devel'
  Allow using custom end-effector
  See merge request robots/tiago_simulation!69
* Allow using custom end-effector
* Contributors: davidfernandez, victor

2.0.21 (2020-02-26)
-------------------

2.0.20 (2019-11-04)
-------------------

2.0.19 (2019-10-23)
-------------------

2.0.18 (2019-10-15)
-------------------

2.0.17 (2019-10-15)
-------------------

2.0.16 (2019-10-10)
-------------------

2.0.15 (2019-09-25)
-------------------

2.0.14 (2019-09-23)
-------------------

2.0.13 (2019-09-23)
-------------------

2.0.12 (2019-08-07)
-------------------
* Merge branch 'better-control' into 'erbium-devel'
  Change PID and tolerances for better tiago simulation
  See merge request robots/tiago_simulation!56
* Change PID and tolerances for better tiago simulation
* Contributors: Victor Lopez

2.0.11 (2019-08-01)
-------------------
* Merge branch 'add-extra-joints-torque-joint-state' into 'erbium-devel'
  Add extra joints to joint_torque_states
  See merge request robots/tiago_simulation!54
* Add extra joints to joint_torque_states
* Contributors: Victor Lopez

2.0.10 (2019-07-17)
-------------------

2.0.9 (2019-07-09)
------------------
* Merge branch 'add-wsg-controller-gazebo' into 'erbium-devel'
  Add missing wsg controller config
  See merge request robots/tiago_simulation!52
* Add missing wsg controller config
* Contributors: Victor Lopez

2.0.8 (2019-07-03)
------------------

2.0.7 (2019-06-17)
------------------

2.0.6 (2019-03-26)
------------------

2.0.5 (2019-03-14)
------------------
* Fix hardware config for wsg
* Contributors: Victor Lopez

2.0.4 (2019-02-26)
------------------
* Add use_moveit_camera
* Contributors: Victor Lopez

2.0.3 (2019-01-23)
------------------

2.0.2 (2019-01-23)
------------------
* Remove usages of pass_all_args, not supported in kinetic yet
* Contributors: Victor Lopez

2.0.1 (2018-12-20)
------------------
* Add missing pass_all_arguments
* Contributors: Victor Lopez

2.0.0 (2018-12-19)
------------------
* Merge branch 'specifics-refactor' into 'erbium-devel'
  Add advanced navigation option to tiago_navigation.launch
  See merge request robots/tiago_simulation!45
* Adapt launch files to new args
* Refactor controller configuration
* Contributors: Victor Lopez

1.0.11 (2018-11-26)
-------------------

1.0.10 (2018-11-26)
-------------------

1.0.9 (2018-10-26)
------------------

1.0.8 (2018-09-28)
------------------

1.0.7 (2018-07-30)
------------------

1.0.6 (2018-07-06)
------------------

1.0.5 (2018-06-05)
------------------
* Merge branch 'add-simple-grasping-action' into 'erbium-devel'
  Add missing simple_grasping_action dependency
  See merge request robots/tiago_simulation!35
* Add missing simple_grasping_action dependency
* Contributors: Victor Lopez

1.0.4 (2018-05-16)
------------------
* Merge branch 'launch-har-arm' into 'erbium-devel'
  Launch controllers depending on robot's arm exists
  See merge request robots/tiago_simulation!33
* Launch controllers depending on robot's arm exists
* Merge branch 'iron-config' into 'erbium-devel'
  Add config for TIAGo Iron
  See merge request robots/tiago_simulation!32
* Add config for TIAGo Iron
* Contributors: Hilario Tome, davidfernandez

1.0.3 (2018-04-10)
------------------
* Merge branch 'extra_joints' into 'erbium-devel'
  added extra joints in joint state controller for simulation
  See merge request robots/tiago_simulation!30
* added extra joints in joint state controller for simulation
* Contributors: Hilario Tome

1.0.2 (2018-03-29)
------------------

1.0.1 (2018-03-26)
------------------
* Merge branch 'recover-chessboard-tiago' into 'erbium-devel'
  Add missing files for tiago_chessboard configurations
  See merge request robots/tiago_simulation!29
* Add missing files for tiago_chessboard configurations
* Contributors: Victor Lopez

1.0.0 (2018-03-26)
------------------
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
