# Hotel Room Delivery Robot
This project involves using a robot to automate the delivery to hotel rooms from kitchen. We use a differential drive robot. The path planning is done using the standard navigation stack. We use SARSA(a reinforcement learning method) to optimise the delivery order. 

Firstly, we need a model of robot to simulate the real life robot. Here we designed a robot using fusion360, and imported it into gazebo since we are using ROS_noetic as the tech-stack for the project. We then designed a simple world, using gazebo. The designed world a 3d map of the hotel environment to which the robot is spawned. After that, the navigation-stack is used to enabale the robot scan the world and make a 2d map(.yaml file). This enables the robot to travel through any new environment. After a map is obtained, then we use the 2d goal publishing function to give a co-ordinate as goal to the robot. Then, the robot will move to the given co-ordinate using the inbuilt planners for autonomous navigation from the navigation-stack. Now, the robot is capable of delivering to any rooms given the co-ordinates of that room(we abstract the details of delivering i.e. reaching the co-ordinate is equivalent to sucessfull delivery). Next we want the robot to optimise the delivery orders for a given set of deliveries !! We can do this in two ways: we can optimise based on distance or based on time. What we want to do is to minmise the delivery time to each customer and the overall delivery time. Therefore rather than taking distance, we take time to delivery to each customer as basis for optimisation. We assign a reward for a delivery based on time of delivery. The total rewards accumilated is sum of rewards of individual deliveries. The aim of the Robot is to maximise the total reward. Since we want to minimise time, we model reward as a monotincally decreasing function of time. 
The following shows an extreme case in which the robot has to deliver to all the rooms. The rooms are dvided into priority and normal rooms. There fore the robot delivers to the priority rooms initially and then delivers to rest of the rooms.

https://user-images.githubusercontent.com/80470473/214027364-b3640950-26fc-4c9f-8ec5-457f1f1ad260.mp4

![myrobot v2](https://user-images.githubusercontent.com/34794384/128828685-a920a91f-5c05-4c24-ba0a-f219379fc0f2.png)

### Simple differential drive robot modelled in Fusion360
### Converted to URDF using fusion2urdf plugin.





