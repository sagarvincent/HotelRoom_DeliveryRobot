#!/usr/bin/python3

import rospy
from geometry_msgs.msg import PointStamped
import tf
import random
import numpy as np
import pandas as pd

class co_ord():

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.room_coordinates = [[8.119316101074219,-3.1443674564361572,0.0032825469970703125]]
        
        
    def callback(self,msg):
        point = PointStamped()
        point.header.stamp = rospy.Time.now()
        point.header.frame_id = "/map"
        point.point.x = msg.point.x
        point.point.y = msg.point.y
        point.point.z = msg.point.z
        
        self.room_coordinates.append([point.point.x,point.point.y,point.point.z])
        

    def listener(self, n_room):
        rospy.init_node('goal_publisher', anonymous=True)
        rospy.point_pub = rospy.Subscriber('/clicked_point', PointStamped, self.callback)
        while(len(self.room_coordinates)< (n_room+1)):
            i=0 #rospy.spin()
    def full_ord(self):

        return self.room_coordinates
    
        

if __name__ == '__main__':

    co_ord = co_ord()
    co_ord.listener(21)
    nd_coord = np.asarray(co_ord.full_ord())
    print(nd_coord)
    pd.DataFrame(nd_coord).to_csv('room_coordinates.csv')