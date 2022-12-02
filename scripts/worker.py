import numpy as np
import state 
import random



##  ------ This is a class for handling several functions that are used to support the other operations ------  ##

# no_of_rooms - total no. of rooms in floor plan
# q_arr - an array storing the q-values of each state-action value function [Q(s,a)]
# alpha - learning rate, which is a hyperparameter to be tuned by user.    -- affects rate of learning
# gamma - discount rate, which is another hyperparamter to be tuned by us. -- determines the effect of future rewards on current actions
class worker():

    def __init__(self, no_of_rooms,  alpha, gamma):
        self.no_of_rooms = no_of_rooms
        self.alpha = alpha
        self.gamma = gamma
        self.q_arr = []
        self.ephsilon = 2
        
        

    # gets the estimated maximum state-action reward from the current room
    def get_est(self, curr_room,q_arr,del_set):
        self.q_arr = q_arr
        max = 0
        for i in del_set:
            if self.q_arr[curr_room][i] > max:
                max = self.q_arr[curr_room][i]
        return max
    # returns the q-value array
    def update_q(self,pre_room,curr_room,reward,q_arr,del_set):
        
        
        self.q_arr = q_arr
        a = self.q_arr[pre_room][curr_room] 
        # estimated future reward from current room
        f_reward = self.get_est(curr_room,q_arr,del_set)
        #check if the error is below a threshold
        if ((reward+(self.gamma*f_reward))-a) < self.ephsilon:
            return 
        else:
            # update the reward using q-learning formula
            a = a + self.alpha*((reward+(self.gamma*f_reward))-a)
            self.q_arr[pre_room][curr_room] = a 
    # returns the chosen action for a given delivery set and current room.
    def choose_action(self,del_set,q_arr,curr_room):
        max = 0
        action = 0
        #select a value randomly which is later used in deciding whether action is to be taken randomly
        prob = random.randint(0,1)
        #if value is 1 action is taken according to policy
        if prob == 1:
            for i in range(len(del_set)):
                w = del_set[i]
                q_val = q_arr[curr_room][w]
                #print(curr_room,w,q_arr)
                if q_val > max:
                    max = q_val
                    action = w
        #if value is zero and there are elements left to deliver then action is chosen randomly
        elif len(del_set) != 0:
            #choosing the action randomly
            action = np.random.choice(del_set, replace=False)
        
        return action

    






