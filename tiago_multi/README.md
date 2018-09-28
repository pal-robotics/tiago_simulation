# Multiple Tiago simulation

This project contains several launch files to simulate multiple Tiago robots in a single Gazebo environment. 

## The environment

In order to have multiple Tiago robots coexisting in the same environment some modifications need to be done. All the nodes belonging to a specific robot are pushed into its own namespace. In addition its tf tree is prepended with the same name as a tf\_prefix.

This generates a single tf tree that has a map root, and then, for each robot, a classic robot/map -> robot/odom -> robot/base\_footprint tree, were robot is this robot's tf\_prefix.

## Launchfiles

The launch files in this package allow you to: launch a Tiago in a specific namespace (with or without navigation), with its tf tree prefixed with the provided namespace; launch a key\_teleop node on a specific namespace; and finally an example with two Tiago robots in the pal office environment (with or without navigation).

### teleop_tiago.launch

Utility launch that runs a key_teleop node in the namespace provided in the *robot* parameter.

### launch_tiago.launch & launch_tiago_navigation.launch

Those are the main launch files of this package. The launch files contain all the required arguments to launch a new Tiago in its own namespace, adding the model to gazebo, launching its controllers and, in case, launch its navigation stack. The launch file has three mandatory parameters:

* *robot_name* Namespace to which this robot's nodes will be pushed (its tf tree will use the same name as the tf\_prefix).
* *x_pose* X coordinate of the initial pose of the robot on the map.
* *y_pose* Y coordinate of the initial pose of the robot on the map. It is important to make sure that the different robots start at different coordinates of the map to avoid overlapping.

In addition the following parameters may be modified:

* *robot* Model of robot to be instantiated (either steel or titanium, for gripper or hand respectively). Default: steel.
* *world* Gazebo world that will be used. Default: small_office.
* *map* Map file for amcl. Default: ~/.pal/tiago\_maps/configurations/small\_office
* *public_sim* Set to true when using the public version of the Tiago simulation. This parameter should not be changed.

For the navigation launch, in addition, the following parameters may be modified:

* *planner* Planner for the navigation. Default: base (move\_base planner).
* *global_planner* Global navigation planner. Default: global_planner.
* *local_planner* Local navigation planner. Default: eband (eband\_planner).
* *localization* Localizacion stack. Default: amcl.

### multitiago_gazebo.launch & multitiago_gazebo.launch

Those launch files launches two default Tiago robots in a pal\_office environment. They may be used as an example on how to build your specific multi-robot launch.
