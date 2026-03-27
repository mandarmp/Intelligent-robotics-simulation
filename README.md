# Intelligent-robotics-simulation
Basic simulation for the intellegient robotics assignment.
Simulation with turtlebot3 in cafe with 8 tables.

Prerequisites:

You will need the tutlebot3, turtlebot3_msgs and turtlebot3_simulations repository downloaded.

Do this run this command in your workspace folder to clone the turtlebot

`git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git`

similarly clone the other two turtle bot repos.

Clone/download our reposity and add the my_simluations folder in your catkin_ws

Then run catkin_make.

To launch the simulation run in separate terminals:

`roslaunch my_simluations my_world.launch`

Also press the play button in Gazebo to start the simulation before running the localisation

`roslaunch my_simluations turtlebot_localisation.launch`


`roslaunch my_simluations main.launch`


`rosrun my_simluations robot_onboard_UI.py`


localise your robot using teleop and the above localisation node.

Run the pathfinder to navigate the robot to the particular tables to serve and clear.

`rosrun my_simluations pathfinder_.py`

hint: make all the python files under the my_simualtions/src as executable.
