cmake_minimum_required(VERSION 2.8.3)
project(tiago_multi)
find_package(catkin REQUIRED COMPONENTS)
catkin_package()

foreach(dir config launch)
    install(DIRECTORY ${dir}/
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

