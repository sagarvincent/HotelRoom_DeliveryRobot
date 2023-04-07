import state
import worker
import numpy as np
import random

import subprocess 

import pandas as pd 
from move_base_msgs.msg import *
from geometry_msgs.msg import * 
import time 
from nav_to_pose import cooo
import rospy
import math 

class man():

    def __init__(self):

        #take the no. of rooms as input
        self.n_rooms = 22 

        ######## ----- Initializing datastorages structures ----- ########

        # initialize the p_time array or load the array stored as csv file
        self.p_arr = pd.read_csv('time-value.csv')#np.zeros((n_rooms,n_rooms))
        self.p_arr = self.p_arr.iloc[:,1:]
        self.p_arr = self.p_arr.to_numpy()
        
        # initialise the q_value array
        self.q_arr = pd.read_csv('q-value.csv')#np.zeros((n_rooms,n_rooms))
        self.q_arr = self.q_arr.iloc[:,1:]
        self.q_arr = self.q_arr.to_numpy()

        # initialize the no. of visit array for average time
        self.p_time_visit = np.zeros((self.n_rooms,self.n_rooms))

        # room_state array
        self.r_arr = []

        # room piority array
        self.prior = [0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0]


        # initializing each room state
        for i in range(self.n_rooms):
            #e = input("enter priority of room ")
            st = state.state(self.prior[i])
            self.r_arr.append(st)

        # learning rate
        self.alpha = .5 #input("Enter the learning rate:")
        # discount rate
        self.gamma = .8 #input("Enter the discount value")

        # creating a worker class object
        self.Worker = worker.worker((self.n_rooms),self.alpha, self.gamma)


    ##### ------------- Defining the function to train the model ----------- #####


    def trainer(self):

        #no. of times the robot goes on delivery or the no. of delivery cycles
        epoch =  30000 #input("Enter the number of epochs")

        #training the model or estimating the q-values for the state
        for _ in range(epoch):

            # print the no. of epochs
            print("epoch no.",_)

            # total reward the robot gets in a single delivery cycle
            total_reward = 0 

            # create an array to store the order in which the delivery is made.
            mod_del = []

            # initializing a variable to hold current room number
            curr_room = 0

            # initializing a variable to hold the previous room number -- needed for updating q-value
            pre_room = 0                 
            
            # randomly choosing the no. of rooms in a single delivery
            n = random.randint(1,self.n_rooms-9)
            # choosing 'n' rooms by random sampling(we choose the rooms to deliver to by randomly picking room numbers)
            del_set = random.sample(range(1,self.n_rooms),n)            
            
            # display the rooms to which the delivery 
            print(del_set)  

            arr = []

            # condition for checking if there is still room to deliver to
            while(len(del_set)>0):

                # set previous room to current room
                pre_room = curr_room        

                # removing the visited room from array except for the first case, which is not in delivery set
                if len(del_set) != 0:    
                    # ensuring its not room zero  -->this is needed since removing room zero which is not present gives error
                    if curr_room != 0:
                        # removing the visited room                
                        del_set.remove(curr_room)
                
                # set current room to the action we took based on q-value
                curr_room = self.Worker.choose_action(del_set,self.q_arr,curr_room)

                # increamenting the no. of visit from pre_room to curre_room
                self.p_time_visit[pre_room][curr_room] = self.p_time_visit[pre_room][curr_room] + 1

                # appending the visted room to know the order of visiting/delivery
                mod_del.append(curr_room)  
                

                     
                ##### ------ ROS code for controlling operations of robot ----- #####

                #take the co-ordinates of current room from csv file and make a Pose object
                try:
                    # initialise the mov_base node
                    rospy.init_node('movebase_client_py')\

                    My_class = cooo()

                    room_lsit = My_class.roomlist()
                    length = len(room_lsit)
                    My_class.amcl_poses()   
                    #time_Elapsed_for_each_room=np.zeros((length+1,length+1))        #print("pose",My_class.posx)    
                    i=0
                    while i<length:
                        print("going to room no:",curr_room)
                        current_goal=room_lsit[curr_room]
                        start = time.time()
                        print(start)
                        result = My_class.movebase_client(current_goal)
                        print("pose",My_class.posx,My_class.posy) 
                        
                        r_target_x=round(My_class.goal.target_pose.pose.position.x,2)
                        r_target_y=round(My_class.goal.target_pose.pose.position.y,2)
                        print("targets",r_target_x,r_target_y)
                
                        if result and (math.isclose(r_target_x,My_class.posx,abs_tol=0.3) and math.isclose(r_target_y,My_class.posy,abs_tol=0.3)):
                            rospy.loginfo("Goal execution done!")
                            i+=1
                            end= time.time()
                            p_time =end-start 
                            self.p_arr[pre_room][curr_room] = p_time
                            
                    print(self.p_arr)    
                except rospy.ROSInterruptException:
                        rospy.loginfo("Navigation test finished.")
                # get the time taken from previous state to this state
                

                #store the p_time for current combination of rooms
                #p_arr[pre_room][curr_room] = (p_arr[pre_room][curr_room]*(p_time_visit[pre_room][curr_room] - 1) + p_time)/(p_time_visit[pre_room][curr_room])
                #take the state of the previous room from state array
                s = self.r_arr[pre_room]        
                reward = s.cal_reward(p_time)
                total_reward = total_reward + reward      
                #update the q-value of the previous state
                self.Worker.update_q(pre_room,curr_room,reward,self.q_arr,del_set )

                print(total_reward)
                print(mod_del)
            """

            subprocess.run(["./reset_robot.sh"]) 
            
            pub = rospy.Publisher('/initialpose', geometry_msgs.msg.PoseWithCovarianceStamped, queue_size=10)
            #rospy.init_node('talker', anonymous=True)
            rate = rospy.Rate(1) # 10hz

            pose = geometry_msgs.msg.PoseWithCovarianceStamped()
            pose.header.frame_id = "map"
            pose.pose.pose.position.x=0.0
            pose.pose.pose.position.y=0.0
            pose.pose.pose.position.z=0.0
            pose.pose.covariance=[0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]
            pose.pose.pose.orientation.z=0.0267568523876
            pose.pose.pose.orientation.w=0.999641971333
            rospy.loginfo(pose)
            pub.publish(pose)"""


        
                
        print(self.q_arr)
        np.savetxt("q-value.csv", self.q_arr, delimiter=",")
        np.savetxt("time-value.csv", self.p_arr, delimiter=",")

    def test(self):

        order_no = int(input("Enter no. of orders: "))
        order_list = []
        for i in range(order_no):
            o = int(input("Enter room no. :"))
            order_list.append(o)
        
        del_set = order_list 
        #total reward the robot gets in a delivery
        total_reward = 0 

        #create an array to store the order in which the delivery is made.
        mod_del = []

        #initializing a variable to hold current room number
        curr_room = 0
        #initializing a variable to hold the previous room number -- needed for updating q-value
        pre_room = 0
        
        arr = []
        #condition for checking if there is still room to deliver to
        while(len(del_set)>0):

            #set previous room to current room
            pre_room = curr_room        

            #removing the visited room from array except for the first case.
            #in the first case, the robot starts from initial position, which is taken as room zero
            #room 0 is not in the delivery set
            if len(del_set) != 0:    
                #ensuring its not room zero
                if curr_room != 0:
                    #removing the visited room                
                    del_set.remove(curr_room)
            
            #set current room to the action we took based on q-value
            curr_room = self.Worker.choose_action(del_set,self.q_arr,curr_room)
            #increamenting the no. of visit from pre_room to curre_room
            self.p_time_visit[pre_room][curr_room] = self.p_time_visit[pre_room][curr_room] + 1
            #appending the visted room to know the order of visiting/delivery
            mod_del.append(curr_room)  
            

                    
            
            #take the co-ordinates of current room from csv file and make a Pose object
            try:
                rospy.init_node('movebase_client_py')\

                My_class = cooo()

                room_lsit = My_class.roomlist()
                length = len(room_lsit)
                My_class.amcl_poses()   
                #time_Elapsed_for_each_room=np.zeros((length+1,length+1))        #print("pose",My_class.posx)    
                i=0
                while i<length:
                    print("going to room no:",curr_room)
                    current_goal=room_lsit[curr_room]
                    start = time.time()
                    print(start)
                    result = My_class.movebase_client(current_goal)
                    print("pose",My_class.posx,My_class.posy) 
                    
                    r_target_x=round(My_class.goal.target_pose.pose.position.x,2)
                    r_target_y=round(My_class.goal.target_pose.pose.position.y,2)
                    print("targets",r_target_x,r_target_y)
            
                    if result and (math.isclose(r_target_x,My_class.posx,abs_tol=0.3) and math.isclose(r_target_y,My_class.posy,abs_tol=0.3)):
                        rospy.loginfo("Goal execution done!")
                        i+=1
                        end= time.time()
                        p_time =end-start 
                        self.p_arr[pre_room][curr_room] = p_time
                        
                print(self.p_arr)    
            except rospy.ROSInterruptException:
                    rospy.loginfo("Navigation test finished.")
            # get the time taken from previous state to this state
            

            #store the p_time for current combination of rooms
            #p_arr[pre_room][curr_room] = (p_arr[pre_room][curr_room]*(p_time_visit[pre_room][curr_room] - 1) + p_time)/(p_time_visit[pre_room][curr_room])
            #take the state of the previous room from state array
            s = self.r_arr[pre_room]        
            reward = s.cal_reward(p_time)
            total_reward = total_reward + reward      
            #update the q-value of the previous state
            #self.Worker.update_q(pre_room,curr_room,reward,self.q_arr,del_set )

            


if __name__ == '__main__':

    m = man() 
    i = input("trainer or tester :")
    if i == "trainer":
        m.trainer()
    elif i == "tester":
        m.test()

        
