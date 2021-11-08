import pygame
import random
import time
import math

board_size_x = 1920
board_size_y = 1090

class Person:
    def __init__(self):
        self.immune = False
        self.infected = False
        self.healthy = True
        self.location = (random.randint(0,board_size_x),random.randint(0,board_size_y))
        self.traveled_for = 501
        self.travel_stop = random.randint(0,250)
        self.direction = (0,0)
        self.color = (50,255,255)
        self.get_direction()

    def get_direction(self):
        if self.traveled_for > self.travel_stop:
            new_dir = random.randint(0,62831)/10000
            self.direction = (math.cos(new_dir),math.sin(new_dir))
            print(self.direction)
            self.traveled_for = 0
            self.travel_stop = random.randint(0,250)
            return
        else:
            self.traveled_for += 1
            x,y = self.location
            self.location = (x+self.direction[0], y+self.direction[1])
            return


class Simulation:
    def __init__(self,size):
        self.size = size
        self.individuals = [Person() for i in range(0,size)]

    def run(self):
        pygame.init()
        window = pygame.display.set_mode((board_size_x,board_size_y))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            window.fill((0,0,0))
            for person in self.individuals:
                pygame.draw.circle(window,person.color,person.location,3)
                person.get_direction()
            pygame.display.flip()




s = Simulation(int(input("size")))
s.run()
