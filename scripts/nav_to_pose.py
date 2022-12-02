#!/usr/bin/python3


import rospy,csv,math,time
from geometry_msgs.msg import PoseWithCovarianceStamped
import numpy as np
# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
class cooo():
    def __init__(self):
        self.posx=None
        self.posy=None
        self.goal=None

    def movebase_client(self,pose):
        #print("pose",pose)
        #print(type(pose[1]))
    # Create an action client called "move_base" with action definition file "MoveBaseAction"
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    
    # Waits until the action server has started up and started listening for goals.
        self.client.wait_for_server()

    # Creates a new goal with the MoveBaseGoal constructor
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
    # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
        self.goal.target_pose.pose.position.x = float(pose[1])
        self.goal.target_pose.pose.position.y=float(pose[2])
        self.goal.target_pose.pose.position.z=float(pose[3])

    # No rotation of the mobile base frame w.r.t. map frame
        self.goal.target_pose.pose.orientation.x =0.0
        self.goal.target_pose.pose.orientation.y =0.0
        self.goal.target_pose.pose.orientation.z =float(pose[6])
        self.goal.target_pose.pose.orientation.w =float(pose[7])

    # Sends the goal to the action server.
        self.client.send_goal(self.goal)
        print("goal sent",self.goal)
    # Waits for the server to finish performing the action.
        self.wait = self.client.wait_for_result()
    # If the result doesn't arrive, assume the Server is not available
        if not self.wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
        # Result of executing the action
            return self.client.get_result()  


    def roomlist(self):
        room_list=[]
            # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        with open("my_poses.csv") as f:
            csreader=csv.reader(f)
            for i in csreader:
                #print(i)
                room_list.append(i)
        return room_list
    
    def callback(self,msg):
        
        self.posx=msg.pose.pose.position.x
        self.posy=msg.pose.pose.position.y
        #print(self.posx,self.posy)
        self.posx=round(self.posx,2)
        self.posy=round(self.posy,2)
        #print("posx and y",self.posx,self.posy)
        #return posx
        
        

    def amcl_poses(self):
        sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped,self.callback)
        



 

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
        
        rospy.init_node('movebase_client_py')
        My_class=cooo()
        room_lsit=My_class.roomlist()
        length = len(room_lsit)
        My_class.amcl_poses()   
        time_Elapsed_for_each_room=np.zeros((length+1,length+1))        #print("pose",My_class.posx)    
        i=0
        while i<length:
            print("going to room no:",i)
            current_goal=room_lsit[i]
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
                time_elapsed =end-start 
                time_Elapsed_for_each_room[i-1][i] = time_elapsed
                
        print(time_Elapsed_for_each_room)    
    except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")
