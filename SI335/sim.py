import random
import pygame
import time
import matplotlib.pyplot as plt
import math
import numpy as np

y_vals = []
class Molecule:
    def __init__(self,t_min, t_max, t, sim):
        self.temperature = t
        self.speed = self.temperature / 100
        self.color = (255*((t-t_min)/(t_max-t_min)),240-100*pow(.2,t/20),255*(1-((t-t_min)/(t_max-t_min))))
        self.position = (float(random.randint(0, sim.width)),float(random.randint(0,sim.height)))
        self.direction = ((init := random.uniform(-1,1)) * self.speed, math.sqrt(1-pow(init,2))* self.speed)
    def temp_update(self, sim):
        if self.position[0] < 0 or self.position[0] > sim.width:
            self.direction = (-self.direction[0], self.direction[1])
        elif self.position[1] < 0 or self.position[1] > sim.height:
            self.direction = (self.direction[0], -self.direction[1])
    def step(self):
        self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
    def place(self, x, y):
        self.position = (x,y)
    def draw(self, simulator):
        pygame.draw.circle(simulator.window,self.color,self.position,3 )
    def check_collisions(self,sim):
        for molecule in sim.molecules:
            if molecule == self:
                continue
            mx, my = molecule.position
            sx, sy = self.position
            dx, dy = (sx-mx,sy-my)
            if dist:= math.sqrt(pow(dx,2) + pow(dy,2)) > 2:
                continue
            else:
                print(str(self.position) + " " + str(molecule.position))

                self.color = (0,255,0)
                molecule.color = (255,0,0)
                self.draw(sim)
                molecule.draw(sim)
                pygame.display.update()
                if abs(dx) < .001:
                    print("hit")
                    print(math.atan(dy/.001))
                else:
                    print(math.atan(dy/dx))
                input()
                sim.window.fill(sim.background_color)
                pygame.display.update()






class Sim:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.t_mid = 100 #float(input("mean temperature: "))
        self.t_spread = 100 #float(input("temperature spread: "))
        self.t_max = self.t_mid + (self.t_spread/2)
        self.t_min = self.t_mid - (self.t_spread/2)
        self.molecules = []
        pygame.init()


        ## WINDOW VARS
        self.running = True
        self.window = pygame.display.set_mode((self.width, self.height))
        self.background_color = (0,0,0)



    def build_sim(self):
        self.n_size = 1000 #int(input("simulation size: "))
        y = [0 for x in range(int(self.t_max))]
        set = np.random.normal(self.t_mid, self.t_spread/6, self.n_size)
        for molecule in range(self.n_size):
            t_calculated = set[molecule]
            if t_calculated < self.t_min:
                t_calculated = self.t_min
            elif t_calculated > self.t_max:
                t_calculated = self.t_max
            self.molecules.append(Molecule(self.t_min, self.t_max, t_calculated, self))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
            self.window.fill(self.background_color)

            for molecule in self.molecules:
                molecule.check_collisions(self)
                molecule.temp_update(self)
                molecule.step()
                molecule.draw(self)

            pygame.display.update()
            time.sleep(.01)

        pygame.quit()

    def temperature(self):
        return self.t_mid + random.uniform(-1,1)*self.t_spread*.5

s = Sim()
s.build_sim()
s.run()
