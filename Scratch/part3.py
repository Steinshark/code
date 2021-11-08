#!/usr/bin/python3

import math
import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *
from primitives import *
from makeTopoMap import *
from itertools import permutations

def on_interval(arg_a):
    pass


class Scene:
    # Initialize and run our environment
    def __init__(self, width=1920, height=1080, caption="Would you like to play a game?", resizable=False):
        # Build the OpenGL / Pyglet Window
        config = pyglet.gl.Config(double_buffer=True)
        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption, config=config)

        # Fix transparent issue...
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Schedule the event
        pyglet.clock.schedule_interval(on_interval,1.0/60.0)


        #####     ##     ##     ##     ##     ##     #####
        #####     Lab Specific Things Start Here     #####
        #####     ##     ##     ##     ##     ##     #####
        self.window_width = width
        self.window_height = height


        ###    Parameters    ###
        self.matrix_rows = 9*5
        self.matrix_cols = 16*5
        self.threshold = [.5 + i for i in range(0,20)]
        self.seed = 3
        self.delta = 2
        self.max_val = 20
        ###    ##########    ###

        self.drawings = []

        self.draw_map()

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():
            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            glFrustrum()
            glMatrixMode(gl.GL_MODELVIEW)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            for points,color in self.drawings:
                glColor3f(color,color,color)
                draw_lines(points)

        @self.window.event
        def on_mouse_press(x,y,button,mods):
            pass
        @self.window.event
        def on_mouse_drag(x,y,dx,dy,button,mods):
            pass
        @self.window.event
        def on_mouse_release(x,y,button,mods):
            pass
        @self.window.event
        def on_key_press(symbol,modifiers):
            #easy screenshot tool
            if symbol == pyglet.window.key.S:
                pyglet.image.get_buffer_manager().get_color_buffer().save(input('fname: ')+'.png')

    # builds the matrix then calls march()
    def draw_map(self):
        self.map_matrix = get_matrix(seed=self.seed,rows=self.matrix_rows,cols=self.matrix_cols,delta=self.delta,maxval=self.max_val)
        self.march()

    # go through every square on the matrix and find contour lines to draw
    def march(self):
        # this is just to make the indexing look a little neater
        m = self.map_matrix

        # run through each square in the matrix
        for t in self.threshold:
            for row in range(0, len(self.map_matrix)-1):
                for col in range(0,len(self.map_matrix[0])-1):
                    square = [[m[row][col],m[row][col+1]],[m[(row+1)][col],m[(row+1)][col+1]]]
                    points = {i:list(self.build_points(row,col))[i] for i in [0,1,2,3]}
                    points_loc = []

                    # This tracks around the square of points
                    #                                 | 0 1 |
                    #                                 | 2 3 |
                    for p1,p2 in [(0,1),(1,3),(3,2),(2,0)]:

                        ## Useful Things to Know
                        p1_height = square[p1//2][p1%2]
                        p2_height = square[p2//2][p2%2]

                        p1_point = points[p1]
                        p2_point = points[p2]

                        dx = abs(p1_point[0]-p2_point[0])
                        dy = abs(p1_point[1]-p2_point[1])
                        dz = abs(p1_point[2]-p2_point[2])
                        ## End useful Things to Know


                        # A very messy way of keeping track of what math needs to go on.
                        # Many cases considering whether we are going from a high point to
                        # a low point or vice-versa, adding the y_value or subtracting it,
                        # etc...

                        if p1_height >= t and p2_height <= t:
                            scale = 1.0-self.interpolate(p1_height,p2_height,t)
                            if p1 == 0:
                                point = (p1_point[0]+dx*scale,p1_point[1],t)
                            elif p1 == 1:
                                point = (p1_point[0],p1_point[1]-dy*scale,t)
                            elif p1 == 3:
                                point = (p1_point[0]+dx*-1*scale,p1_point[1],t)
                            elif p1 == 2:
                                point = (p1_point[0],p1_point[1]+dy*scale,t)
                            points_loc.append(point)

                        elif p2_height >= t and p1_height <= t:
                            scale = self.interpolate(p2_height,p1_height,t)
                            if p1 == 0:
                                point = (p1_point[0]+dx*scale,p1_point[1],t)
                            elif p1 == 1:
                                point = (p1_point[0],p1_point[1]-dy*scale,t)
                            elif p1 == 3:
                                point = (p1_point[0]+dx*-1*scale,p1_point[1],t)
                            elif p1 == 2:
                                point = (p1_point[0],p1_point[1]+dy*scale,t)
                            points_loc.append(point)

                    # Sets color based on threshold
                    color = .3 + .05 * self.threshold.index(t)
                    #glColor3f(color,color,color)
                    #draw_lines(points_loc)
                    self.drawings.append((points_loc,color))


    # Interpolates from the high to the low value
    def interpolate(self,high,low,thresh):
        high = float(high)
        low = float(low)
        thresh = float(thresh)
        return abs((thresh-low)) / abs((high-low))

    # Builds a list of points given where we are in the matrix (row,col)
    def build_points(self,row,col):
        row = (self.matrix_rows-1)-row
        unit_distance_vert = float(self.window_height/(self.matrix_rows-1))
        unit_distance_horiz = float(self.window_width/(self.matrix_cols-1))
        ll = (
                (col / (self.matrix_cols-1))*self.window_width,\
                (row / (self.matrix_rows-1))*self.window_height,\
                0\
             )
        lr = (ll[0]+unit_distance_horiz,ll[1],0)
        ul = (ll[0],ll[1]-unit_distance_vert,0)
        ur = (ll[0]+unit_distance_horiz,ll[1]-unit_distance_vert,0)
        return ll,lr,ul, ur


# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    myGame = Scene(1600, 900, "Example")
    #debugging = pyglet.window.event.WindowEventLogger()
    #myGame.window.push_handlers(debugging)
    pyglet.app.run()
