^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package tiago_2dnav_gazebo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.0.23 (2020-07-30)
-------------------
* Merge branch 'rename_tf_prefix' into 'erbium-devel'
  Rename tf_prefix to robot_namespace
  See merge request robots/tiago_simulation!70
* Rename tf_prefix to robot_namespace
* Contributors: davidfernandez, victor

2.0.22 (2020-04-21)
-------------------
* Merge branch 'robot-arg-mapping' into 'erbium-devel'
  enabled robot arg in mapping launch
  See merge request robots/tiago_simulation!68
* enabled robot arg in mapping launch
* Contributors: Procópio Stein, victor

2.0.21 (2020-02-26)
-------------------

2.0.20 (2019-11-04)
-------------------
* Merge branch 'robot_pose_pub' into 'erbium-devel'
  Added robot_pose publisher
  See merge request robots/tiago_simulation!66
* Added robot_pose publisher
* Contributors: Sai Kishor Kothakota, Victor Lopez

2.0.19 (2019-10-23)
-------------------
* Merge branch 'multi-laser-fiter' into 'erbium-devel'
  disable laser filter for multi due to tf_prefix problem
  See merge request robots/tiago_simulation!65
* disable laser filter for multi due to tf_prefix problem
* Contributors: Jordan Palacios, Procópio Stein

2.0.18 (2019-10-15)
-------------------

2.0.17 (2019-10-15)
-------------------
* Merge branch 'refactor' into 'erbium-devel'
  Refactor
  See merge request robots/tiago_simulation!64
* addded rgbd_scan node in main launches
* consolidated public launches
* removed map relays
* Contributors: Procópio Stein, Victor Lopez

2.0.16 (2019-10-10)
-------------------

2.0.15 (2019-09-25)
-------------------

2.0.14 (2019-09-23)
-------------------
* Merge branch 'stockbot-carrot-migration' into 'erbium-devel'
  use vo filling
  See merge request robots/tiago_simulation!59
* use vo filling
* Contributors: Procópio Stein, Victor Lopez

2.0.13 (2019-09-23)
-------------------
* Merge branch 'stockbot-carrot-migration' into 'erbium-devel'
  now uses laser filter to provide scan and scan_raw
  See merge request robots/tiago_simulation!58
* now uses laser filter to provide scan and scan_raw
* Contributors: Procópio Stein, Victor Lopez

2.0.12 (2019-08-07)
-------------------
* Merge branch 'tiago_dual_cfg' into 'erbium-devel'
  Added the parameter toallow the selection of the tiago_dual cfg package for the move_base launch
  See merge request robots/tiago_simulation!57
* Added the parameter toallow the selection of the tiago_dual cfg package for the move_base launch
* Contributors: Victor Lopez, alessandrodifava

2.0.11 (2019-08-01)
-------------------

2.0.10 (2019-07-17)
-------------------

2.0.9 (2019-07-09)
------------------

2.0.8 (2019-07-03)
------------------
* Merge branch 'more_fixes' into 'erbium-devel'
  more fixes on moved launch files
  See merge request robots/tiago_simulation!51
* removed pick_and_place.launch file
* more fixes on moved launch files
* Contributors: Sai Kishor Kothakota, Victor Lopez

2.0.7 (2019-06-17)
------------------
* Merge branch 'new_nav_cfg' into 'erbium-devel'
  moved simulation launches from tiago_2dnav
  See merge request robots/tiago_simulation!50
* moved simulation launches from tiago_2dnav
* Merge branch 'teb_planner' into 'erbium-devel'
  Add TEB planner
  See merge request robots/tiago_simulation!49
* Add TEB planner
* Contributors: Hilario Tome, Sai Kishor Kothakota, Victor Lopez, davidfernandez

2.0.6 (2019-03-26)
------------------

2.0.5 (2019-03-14)
------------------

2.0.4 (2019-02-26)
------------------
* Add rgbd scan to public navigation
* Contributors: Victor Lopez

2.0.3 (2019-01-23)
------------------
* Change default deprecated param to titanium
  For backwards compatibility
* Add more params to public sim
* Contributors: Victor Lopez

2.0.2 (2019-01-23)
------------------
* Merge branch 'fix_default_global_planner' into 'erbium-devel'
  Set default global planner back to global_planner
  See merge request robots/tiago_simulation!46
* Add mapping from deprecated robot to new variables
* Don't launch loc measure on public sim
* Set default global planner back to global_planner
* Contributors: Jordan Palacios, Victor Lopez

2.0.1 (2018-12-20)
------------------

2.0.0 (2018-12-19)
------------------
* Merge branch 'specifics-refactor' into 'erbium-devel'
  Add advanced navigation option to tiago_navigation.launch
  See merge request robots/tiago_simulation!45
* Add more params to map and nav launches
* Adapt launch files to new args
* Refactor controller configuration
* Move tiago navigation code to a separate file for easier overwrite
* Add advanced navigation option to tiago_navigation.launch
* Contributors: Victor Lopez

1.0.11 (2018-11-26)
-------------------
* Merge branch 'add-extra-gz-args-flag' into 'erbium-devel'
  Add extra_gazebo_args flag
  See merge request robots/tiago_simulation!44
* Add extra_gazebo_args flag
* Contributors: Victor Lopez

1.0.10 (2018-11-26)
-------------------
* Merge branch 'add-tuck-arm' into 'erbium-devel'
  Add tuck_arm argument
  See merge request robots/tiago_simulation!43
* Add tuck_arm argument
* Contributors: Victor Lopez

1.0.9 (2018-10-26)
------------------

1.0.8 (2018-09-28)
------------------
* Merge branch 'fix-default-planner' into 'erbium-devel'
  fixed default planner to global_planner
  See merge request robots/tiago_simulation!41
* fixed default planner to global_planner
* Contributors: Jordan Palacios, Procópio Stein

1.0.7 (2018-07-30)
------------------

1.0.6 (2018-07-06)
------------------
* Merge branch 'add-log-recording' into 'erbium-devel'
  Add log recording
  See merge request robots/tiago_simulation!36
* Add log recording
* Contributors: Victor Lopez

1.0.5 (2018-06-05)
------------------

1.0.4 (2018-05-16)
------------------

1.0.3 (2018-04-10)
------------------

1.0.2 (2018-03-29)
------------------

1.0.1 (2018-03-26)
------------------

1.0.0 (2018-03-26)
------------------

0.0.18 (2018-03-21)
-------------------
* Add extra arguments to public simulation launch files
* Contributors: Victor Lopez

0.0.17 (2018-02-20)
-------------------

0.0.16 (2018-02-16)
-------------------

0.0.15 (2018-01-24)
-------------------

0.0.14 (2017-11-07)
-------------------

0.0.13 (2017-11-02)
-------------------
* add argument to choose map
  w
* Contributors: Jordi Pages

0.0.12 (2017-05-30)
-------------------

0.0.11 (2017-05-16)
-------------------
* add world argument
* Contributors: Jordi Pages

0.0.10 (2016-10-21)
-------------------

0.0.9 (2016-10-14)
------------------
* set a different initial pose of the robot
* set myself as maintainer
* launch files to support public map/loc
* disable dynamic_footprint when public_sim=true
* New launch file for the pick and place demo, also provided the world
* Contributors: Jordi Pages, job-1994

0.0.7 (2016-06-15)
------------------
* Change default robot type to custom
* Contributors: Victor Lopez

0.0.6 (2016-06-15)
------------------

0.0.5 (2016-06-15)
------------------

0.0.4 (2016-06-15)
------------------

0.0.3 (2016-06-14)
------------------
* default robot model
* fix default robot
* Contributors: Jeremie Deray

0.0.2 (2015-04-15)
------------------

0.0.1 (2015-04-15)
------------------
* refs #10237 : fixes default robot model to full
* Missing a d in the project name
* adds tiago_2dnav_gazebo
* Contributors: Sammy Pfeiffer, enriquefernandez
