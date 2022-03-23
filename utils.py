# https://www.hindawi.com/journals/jam/2014/659805/

import math
import numpy as np

def SetMagnitude(vec, mag): #Set the magnitude of the vector "vec" to "mag" value
    
        current_mag = math.sqrt(vec[0]**2 + vec[1]**2)
        if current_mag == 0: current_mag=0.01
        return (vec[0] * (mag / current_mag), vec[1] * (mag / current_mag))

def GetMagnitude(vec): #Get the magnitude of the vector "vec"
        return math.sqrt(vec[0]**2 + vec[1]**2)
 
def Euclidian_distance(position1, position2): #Compute the euclidian distance between "position1" and "position2"
        x1 = position1[0]
        y1 = position1[1]
        x2= position2[0]
        y2 = position2[1]
        
        return ((x2-x1)**2 + (y2-y1)**2)**(1/2)

def GetNormal(vec): #Get the normal of the vector "vec"
        return (-vec[1], vec[0])

def oriented_triangle(position, velocity, size): #Compute the three point of the triangle needed to display the agents
        velocity = SetMagnitude(velocity, size)
        velocity_pointy = SetMagnitude(velocity, size*3)
        point1 = np.add(position, velocity_pointy)
        point2 = np.add(position, GetNormal(velocity))
        point3 = np.subtract(position, GetNormal(velocity))
        
        return [point1,point2,point3]
