#! /bin/sh




rostopic pub -1 /gazebo/set_model_state gazebo_msgs/ModelState "model_name: 'myrobot'
pose:
  position:
    x: 0 #8.119316101074219
    y: 0 #-3.1443674564361572
    z: 0 #0.0032825469970703125
"
