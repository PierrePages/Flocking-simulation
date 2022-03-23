import pygame
from pygame.locals import *

from boids import Boid
import utils


white = (255,250,250)
dark_grey = (105,105,105)
red = (255,0,0)
black = (0,0,0)


pygame.display.set_caption("Boids") #Set the title of the window
width, height = 1080,720
window = pygame.display.set_mode((width, height)) #Set the window's size

flock1 = [Boid(width, height, i) for i in range(60)] #initialisation of Flock 1 (white)
flock2 = [Boid(width, height, i) for i in range(40)] #initialisation of Flock 2 (red)

flock_total = flock1+flock2 


def draw_window():
    window.fill(black) #fill the window at each iteration

    for boid in flock1:
        #boid.border() # teleport each boid to the other side of the screen when hit a wall
        boid.border_avoidance()
        boid.separation(flock_total) #flock_total is called here because the separation is computed betwenn all the agents
        boid.cohesion(flock1)
        boid.alignment(flock1)
        boid.update()

        pygame.draw.polygon(window, white,points=utils.oriented_triangle(boid.position, boid.velocity, 3)) 

        if boid.id==1: #Display the perception area
             pygame.draw.circle(window, red,boid.position, boid.perception,1)
 
    
    for boid in flock2:
        #boid.border()
        boid.border_avoidance()
        boid.separation(flock_total)
        boid.cohesion(flock2)
        boid.alignment(flock2)
        boid.update()

        pygame.draw.polygon(window, red,points=utils.oriented_triangle(boid.position, boid.velocity, 3))


    pygame.display.update()


def main():

    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(60) # Fix the maximum FPS
        for event in pygame.event.get(): #check the event list
            if event.type == pygame.QUIT: #When we close the game
                run = False
        
        draw_window()


if __name__ == "__main__": 
   main()
    



pygame.quit()

