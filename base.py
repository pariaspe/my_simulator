#!/usr/bin/env python

import pygame
import time
import sys
from numpy import genfromtxt

RATE = 0.5
GOAL = [8, 8]

class Robot:
    """Basic 2D robot with position and velocity."""
    def __init__(self, pos=[0,0]):
        self.pos = pos
        self.vel = [0, 0]

    def set_vel(self, vel):
        """In px/s"""
        self.vel = [vel[0]*RATE, vel[1]*RATE]


class RobotView(pygame.Rect):
    """View of Robot. Helps to visualize the robot over the screen."""
    COLOR_ROBOT = (255, 0, 0)

    def __init__(self, sim, robot=None):
        """inits rect"""
        self.sim = sim
        self.robot = robot

        self.width = self.sim.cell_width/2.0
        self.height = self.sim.cell_height/2.0

        x = self.sim.cell_width*self.robot.pos[0] + self.sim.cell_width/4.0
        y = self.sim.cell_height*self.robot.pos[1] + self.sim.cell_height/4.0
        super().__init__(x, y, self.width, self.height)

    def update_pos(self):
        """Moves Rect and updates robot pose."""
        self.move_ip(*self.robot.vel)
        x = (self.center[0] - self.sim.cell_width/4.0) / self.sim.cell_width
        y = (self.center[1] - self.sim.cell_height/4.0) / self.sim.cell_height
        self.robot.pos = [x, y]

class Map:
    """Basic Map."""
    def __init__(self, filename):
        self.cells = genfromtxt(filename, delimiter=',')
        self.columns = self.cells.shape[0]
        self.rows = self.cells.shape[1]


class Simulator:
    """Simulator. Displays a screen and keeps it updated."""
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    COLOR_BACKGROUND = (0, 0, 0)
    COLOR_WALL = (255, 255, 255)
    COLOR_ROBOT = (255, 0, 0)

    def __init__(self, map=None):
        """Inits screen. Full black."""
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
        self.screen.fill(self.COLOR_BACKGROUND)

        self.robot = None
        self.map = map

        pygame.display.flip()

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, map_):
        self.__map = map_
        if map_ is not None:
            self.load_map()

    def load_map(self):
        """Loads a map over the screen."""
        self.cell_width = self.SCREEN_WIDTH/self.map.columns
        self.cell_height = self.SCREEN_HEIGHT/self.map.rows

        for i, row in enumerate(self.map.cells):
            for j, cell in enumerate(row):

                if cell == 0:
                    continue

                pygame.draw.rect(self.screen, self.COLOR_WALL, pygame.Rect(self.cell_width*j, self.cell_height*i, self.cell_width, self.cell_height))
        pygame.display.update()

    def load_robot(self, robot):
        """Loads a robot over the screen."""
        self.robot_view = RobotView(self, robot)
        pygame.draw.rect(self.screen, self.COLOR_ROBOT, self.robot_view)
        pygame.display.update()

    def update(self):
        """Updates the screen and objects over it."""
        pygame.draw.rect(self.screen, self.COLOR_BACKGROUND, self.robot_view)
        self.robot_view.update_pos()
        pygame.draw.rect(self.screen, self.COLOR_ROBOT, self.robot_view)
        pygame.display.update()


if __name__ == "__main__":
    # Parse CLI arguments
    if (len(sys.argv) != 4):
        print("./base.py map1.csv 2 2")
        quit()
    inFileStr = sys.argv[1]
    initX = float(sys.argv[2])
    initY = float(sys.argv[3])

    sim = Simulator()
    map = Map(inFileStr)
    sim.map = map

    robot = Robot([1, 1])
    sim.load_robot(robot)
    time.sleep(1)

    robot.set_vel([50.0, 0.0])
    while True:
        if robot.pos[0] >= GOAL[0]:
            robot.set_vel([0.0, 50.0])
        if robot.pos[1] >= GOAL[1]:
            robot.set_vel([0.0, 0.0])
            break

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        sim.update()

        print("Robot at", robot.pos)
        time.sleep(RATE)

    print("GOAL REACHED!")
    time.sleep(1)
    print("BYE!")
