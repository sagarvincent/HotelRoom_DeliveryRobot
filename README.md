# Hotel Room Delivery Robot
This project involves using a robot to automate the delivery to hotel rooms from kitchen. We use a differential drive robot. The path planning is done using the standard navigation stack. We use SARSA(a reinforcement learning method) to optimise the delivery order. 

Firstly, we need a model of robot to simulate the real life robot. Here we designed a robot using fusion360, and imported it into gazebo since we are using ROS_noetic as the tech-stack for the project. We then designed a simple world, using gazebo. The designed world a 3d map of the hotel environment to which the robot is spawned. After that, the navigation-stack is used to enabale the robot scan the world and make a 2d map(.yaml file). This enables the robot to travel through any new environment. After a map is obtained, then we use the 2d goal publishing function to give a co-ordinate as goal to the robot. Then, the robot will move to the given co-ordinate using the inbuilt planners for autonomous navigation from the navigation-stack. Now, the robot is capable of delivering to any rooms given the co-ordinates of that room(we abstract the details of delivering i.e. reaching the co-ordinate is equivalent to sucessfull delivery). Next we want the robot to optimise the delivery orders for a given set of deliveries !! We can do this in two ways: we can optimise based on distance or based on time. What we want to do is to minmise the delivery time to each customer and the overall delivery time. Therefore rather than taking distance, we take time to delivery to each customer as basis for optimisation. We assign a reward for a delivery based on time of delivery. The total rewards accumilated is sum of rewards of individual deliveries. The aim of the Robot is to maximise the total reward. Since we want to minimise time, we model reward as a monotincally decreasing function of time. 
The following shows an extreme case in which the robot has to deliver to all the rooms. The rooms are divided into priority and normal rooms. There fore the robot delivers to the priority rooms initially and then delivers to rest of the rooms.

https://user-images.githubusercontent.com/80470473/214027364-b3640950-26fc-4c9f-8ec5-457f1f1ad260.mp4

# How to run the code in your system
OS: Ubuntu Focal Fossa  (20.04.6 LTS)
ROS : One, Noetic
RAM : 4 GB and above
VRAM : not necessary
Software/Packages required : ROS-noetic, Gazebo, gmapping, navigation-stack, numpy, pandas


1. ROS-noetic installation

`sudo apt update && sudo apt install -y curl gnupg2 lsb-release`
`sudo apt install curl`
`curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -`
`sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'`

`sudo apt update`
`sudo apt install -y ros-noetic-desktop-full`

`sudo rosdep init`
`rosdep update`

`echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc`
`source ~/.bashrc`

`rosversion -d`

2. Navigation stack installation

`sudo apt-get install ros-noetic-navigation`

We need to use amcl package as part of this project. To ensure its properly installed use the follwoing command : rospack find amcl
The output should be : `ros/noetic/share/amcl`
If the output is empty, it means amcl is not on path. If you install amcl seperately you need to add that folder path, if you installed as above, add set the rospath in `~/.bashrc` file as : `export ROS_PACKAGE_PATH=/opt/ros/noetic/share` , then source the file as : `source ~/.bashrc`

As part of this we also have to install the move_base_msgs package. Use the follwoing command :
 `sudo apt-get install ros-noetic-move-base-msgs`
 `source ~/.bashrc`


### Simple differential drive robot modelled in Fusion360 converted to URDF using fusion2urdf plugin.

![myrobot v2](https://user-images.githubusercontent.com/34794384/128828685-a920a91f-5c05-4c24-ba0a-f219379fc0f2.png)





