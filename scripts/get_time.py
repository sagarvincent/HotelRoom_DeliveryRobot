#!/usr/bin/python3


from nav_to_pose import cooo
import rospy 
import time 
import math
import numpy as np


def check_zero(row_val, col_val,tm,):

    ind = 0 
    My_class = cooo()
    My_class.amcl_poses() 
    room_lsit=My_class.roomlist()

    while(ind<col_val):

        if tm[row_val][ind] == 0:

            
            i = 0
            while i<1:

                print("going to room no:",ind)
                current_goal = room_lsit[ind]
                start = time.time()
                print(start)
                result = My_class.movebase_client(current_goal)
                print("pose",My_class.posx,My_class.posy) 
                        
                r_target_x = round(My_class.goal.target_pose.pose.position.x,2)
                r_target_y = round(My_class.goal.target_pose.pose.position.y,2)
                print("targets",r_target_x,r_target_y)
                
                if result and (math.isclose(r_target_x,My_class.posx,abs_tol=0.3) and math.isclose(r_target_y,My_class.posy,abs_tol=0.3)):
                    rospy.loginfo("Goal execution done!")
                    i+=1
                    end = time.time()
                    time_elapsed =end-start 
                    tm[row_val][ind] = time_elapsed
                    tm[ind][row_val] = time_elapsed
                    print(tm)

                    check_zero(ind,col_val,tm)


        else :
            ind = ind + 1 
    if ind == col_val:
        check_zero(row_val+1,col_val, tm)

def room_combo():

    rospy.init_node('movebase_client_py')
    tm = np.zeros((22,22))
    check_zero(0,22, tm)
    np.savetxt("real_time.csv", tm, delimiter=",")
        
          
        

if __name__ == '__main__':
    try:
        room_combo()


    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

    

