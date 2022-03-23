import numpy as np
import random
import utils


class Boid():

    def __init__(self, width, height, id): # define the attributes of each agent
        
        self.id = id
        self.width = width
        self.height = height
        
        self.position = (random.uniform(0,self.width),random.uniform(0,self.height)) #set the initial position randomly somewhere in the screen
        self.velocity = (random.uniform(-2,2),random.uniform(-2,2)) #set the initial velocity randomly
        self.acceleration = (0,0)
        
        self.max_speed = 4
        self.max_steer = 0.3
        
        self.perception = 100
        
        pass
        
    def update(self): #update position speed and acceleration at each iteration
        
        self.velocity = np.add(self.velocity,self.acceleration)
        self.velocity = utils.SetMagnitude(self.velocity, self.max_speed)
        self.position = np.add(self.position,self.velocity)
        self.acceleration = (0,0)

        pass
    
    def getVelocity(self): #used to get the velocity of the agent
        return self.velocity
    
    def border(self): #teleport the agent to the other side of the screen when it cross a wall, not used in the final version

        if self.position[0] > self.width:
            self.position[0] = 0

        elif self.position[0] < 0:
            self.position[0] = self.width
        
        if self.position[1] > self.height:
            self.position[1] = 0

        elif self.position[1] < 0:
            self.position[1] = self.height
        pass


    def border_avoidance(self): #allow the agent to avoid the border of the screen

        x = self.position[0]
        y = self.position[1]

        perception = self.perception/4 #The perception of the agent is reduced otherwise they turn too early

        count = 0
        steering = (0,0)

        if x - perception < 0: #detect the west wall
            direction = (1,0)
            dw = np.multiply(x,x) #the x coordinate is used as the distance between the agent and the wall
            direction = np.divide(direction,dw)
            steering = np.add(steering, direction)
            count += 1

        if  x + perception > self.width: #detect the east wall
            direction = (-1,0)
            de = np.multiply(self.width - x, self.width - x) #the x coordinate is used as the distance between the agent and the wall
            direction = np.divide(direction,de)
            steering = np.add(steering, direction)
            count += 1
            
        if  y- perception < 0: #detect the south wall
            direction = (0,1)
            ds = np.multiply(y,y) #the y coordinate is used as the distance between the agent and the wall
            direction = np.divide(direction,ds)
            steering = np.add(steering, direction)
            count += 1

        if  y + perception > self.height : #detect the north wall
            direction = (0,-1)
            dn = np.multiply(self.height - y, self.height - y) #the y coordinate is used as the distance between the agent and the wall
            direction = np.divide(direction,dn)
            steering = np.add(steering, direction)
            count += 1

        if(count != 0):
            steering[:] = [x / count for x in steering] #Get the average in case the agent is going into a corner
            steering = utils.SetMagnitude(steering, self.max_speed) #Set the steering to max speed because we do not want the agent to decelerate 
            steering = np.subtract(steering, self.velocity) #Steering formula
            steering = utils.SetMagnitude(steering, self.max_steer*10)  #Set the magnitude of the final vector to max steer *10

        self.acceleration = np.add(self.acceleration, steering)
        

        
        pass

    
    def separation(self, boids): #separation function
        steering = (0,0)
        count = 0 
        
        for boid in boids:
            if not np.array_equal(boid.position,self.position): # to check that the agent we are looking at is not himself
                if utils.Euclidian_distance(self.position, boid.position) < self.perception: 
                    difference = np.subtract(self.position, boid.position)
                    d = utils.Euclidian_distance(self.position, boid.position)
                    d = np.multiply(d,d)
                    difference = np.divide(difference,d)
                    steering = np.add(steering, difference)
                    count += 1
        
        if(count != 0):
            steering[:] = [x / count for x in steering]
            steering = utils.SetMagnitude(steering,self.max_speed)
            steering = np.subtract(steering,self.velocity)
            
            if utils.GetMagnitude(steering)> self.max_steer*1.7: #1.7 is an empirical value chosen during the tuning of the simulation
                steering = utils.SetMagnitude(steering, self.max_steer*1.7)
        
        self.acceleration = np.add(self.acceleration,steering)
        
        pass
    
    def alignment(self, boids): #Alignment function
        steering = (0,0)
        count = 0
        for boid in boids:
            if utils.Euclidian_distance(self.position, boid.position)< self.perception:
                steering = np.add(steering,boid.velocity)
                count += 1
                
        if(count != 0):
            steering[:] = [x / count for x in steering]
            steering = utils.SetMagnitude(steering,self.max_speed)
            steering = np.subtract(steering,self.velocity)
            
            if utils.GetMagnitude(steering)> self.max_steer*1.2: #1.2 is an empirical value chosen during the tuning of the simulation
                steering = utils.SetMagnitude(steering, self.max_steer*1.2)
        
        self.acceleration = np.add(self.acceleration,steering)
        
        pass
    
    def cohesion(self, boids): #Cohesion function
        steering = (0,0)
        count = 0

        for boid in boids:
            if utils.Euclidian_distance(boid.position, self.position)< self.perception:
                if not np.array_equal(boid.position,self.position):
                    steering = np.add(steering,boid.position)
                    count += 1
                
        if(count != 0):
            steering[:] = [x / count for x in steering]
            steering = np.subtract(steering,self.position)
            steering = utils.SetMagnitude(steering, self.max_speed)
            steering = np.subtract(steering,self.velocity)
            
            if utils.GetMagnitude(steering)> self.max_steer:
                steering = utils.SetMagnitude(steering, self.max_steer)
        
        self.acceleration = np.add(self.acceleration,steering)

        pass
    
    