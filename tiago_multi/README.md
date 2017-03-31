# Multiple Tiago simulation

This project contains several launchfiles to simulate multiple Tiago robots in a single Gazebo environment. 

## The environment

In order to have multiple Tiago robots coexisting in the same environment some modifications need to be done. All the nodes belonging to a specific robot are pushed into its own namespace. In addition its tf tree is prepended with the same name as a tf\_prefix.

This generates a single tf tree that has a map root, and then, for each robot, a classic robot/map -> robot/odom -> robot/base\_footprint tree, were robot is this robot's tf_prefix.

## Launchfiles

The three launchfiles in this package allow you to: launch a Tiago in a specific namespace, with its tf tree prefixed with the provided namespace; launch a key\_teleop node on a specific namespace; and finally an example with two Tiago robots in a small office environment.

### teleop_tiago.launch

Utility launch that runs a key_teleop node in the namespace provided in the *robot* parameter.

### launch_tiago.launch

This is the main launch of this package. This launchfile contains all the required arguments to launch a new Tiago in its own namespace, adding the model to gazebo and launching both its controllers and its navigation stack. The launchfile has three mandatory parameters:

* *robot_name* Namespace to which this robot's nodes will be pushed (its tf tree will use the same name as the tf_prefix).
* *x_pose* X coordinate of the initial pose of the robot on the map.
* *y_pose* Y coordinate of the initial pose of the robot on the map. It is important to make sure that the different robots start at different coordintes of the map to avoid overlapping.

In addition the following parameters may be modified:

* *robot* Model of robot to be instantiated (either steel or titanium, for gripper or hand respectively). Default: steel.
* *world* Gazebo world that will be used. Default: small_office.
* *planner* Planner for the navigation. Default: base (move_base planner).
* *global_planner* Global navigation planner. Default: navfn.
* *local_planner* Local navigation planner. Default: eband (eband_planner).
* *localization* Localizacion stack. Default: amcl.
* *map* Map file for amcl. Default: ~/.pal/tiago_maps/configurations/small_office
* *public_sim* Set to true when using the public version of the Tiago simulation. This parameter should not be changed.

### multitiago_gazebo.launch

This launchfile launches two default Tiago robots in a small_office environment. It may be used as an example on how to build your specific multi-robot launch.
