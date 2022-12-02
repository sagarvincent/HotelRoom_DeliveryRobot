import numpy as np
import math 



###  --------  inputs required for the complete functioning of the class   --------   ###

# x - x axis coorderinate of the room door in the map 
# y - y axis coorderinate of the room door in the map
# x0 - x axis coorderinate of the robot starting location in the map
# y0 - y axis coorderinate of the robot starting location in the map

# priority - used to imply the importance of rooms, higher priority rooms require better service.

# p_time - the time taken by the robot to reach the room coordinate from the previous state or initial robot location
class state():

    def __init__(self, priority):

        #no. of times a high path is chosen
        self.p_high_count = 0
        #no. of times a low path is chosen
        self.p_low_count = 0
        #average time taken for path high
        self.p_high_mean = 0
        #average time taken for path low
        self.p_low_mean = 0

        #no. of time a room is visited
        self.room_visit = 0
        #limit for classifying as high path and low path
        self.t_limit = 0

        #lowest time taken for reaching the room
        self.p_low = 0
        #highest time taken for reaching the room
        self.p_high = 0
        #time taken for latest visit to the room
        self.p_time = 0
        #percent of low path visit
        self.a_low = 0
        #percent of high path visit
        self.a_high = 0

        #delivery deadline for the room
        self.deadline = 0
        #priority of the room
        self.priority = priority
        #average time taken to reach the room
        self.av_time = 0
        #reward for the latest visit to the room
        self.reward = 0
        #average state value, which is the expected reward--calculated from past visits
        self.av_state_value = 0
        #q-value of the state-action
        self.q_value = 0

        ##  Distance features  ##

        #x & y coordinate of room
        self.x = 0
        self.y = 0
        self.displacment = 0
        self.distance = 0

    #called to calculate reward for a state visit
    def cal_reward(self,p_time):
        #rewardif the delivery is within the deadline
        r_intime = 0
        #reward if the delivery is after the deadline
        r_outtime = 0
        #setting deadline and deliveryrewards according to priority
        if self.priority == 0:
            r_intime = 10
            r_outtime = -5
            self.deadline = 150
        elif self.priority == 1:
            r_intime = 20
            r_outtime = -10
            self.deadline = 150
        #checking if delivery is within deadline
        if p_time > self.deadline:
            r = r_outtime
        elif p_time <= self.deadline:
            r = r_intime
        #returning the calculated reward
        return (r-.025*p_time)

    #called each time a state is visited, to update its state value---- argument is the time taken for latest delivery/visit
    def update_state_val(self,p_time):
        #taking in the latest delivery time
        self.p_time = p_time
        #update the no. of times the room is visited
        self.room_visit = self.room_visit + 1
        #checking and updating the highest and lowest time for visit
        if self.p_time > self.p_high:
            self.p_high = self.p_time
        elif self.p_time < self.p_low:
            self.p_low = self.p_time
        self.t_limit = self.p_low + ((self.p_high - self.p_low)/2)

        #classifying if the path taken is high path or low path
        if self.p_time > self.t_limit:
            #updating the count
            self.p_high_count = self.p_high_count + 1
            #updating the mean
            self.p_high_mean = (((self.p_high_mean*(self.p_high_count-1))  + self.p_time)/self.p_high_count)
        elif self.p_time < self.t_limit:
            #updating the count
            self.p_low_count  = self.p_low_count + 1
            #updating the mean
            self.p_low_mean = (((self.p_low_mean*(self.p_low_count-1)) + self.p_time)/self.p_low_count)

        #updating the percent of low path visit
        self.a_low = ( self.p_low_count/self.room_visit )
        #updating the percent of high path visit
        self.a_high = ( self.p_high_count/self.room_visit )
        #updating the average time taken for visting the room
        self.av_time = self.a_low*self.p_low_mean + self.a_high*self.p_high_mean

        #calculating the reward for latest visit to room
        self.reward = self.cal_reward(self.p_time)
        #updating the average value of the state based on reward recieved
        av_state_value = (((av_state_value*(self.room_visit-1)) + self.reward)/self.room_visit)
