#!/usr/bin/env python

import pygame
import time
import sys
import os
from numpy import genfromtxt
from subprocess import Popen, PIPE
from tools import astar
import argparse

MAP = "map1"
START_X = 2
START_Y = 2
END_X = 8
END_Y = 8

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = LOCAL_PATH + "/{0}.csv"
RATE = 0.5
GOAL = [END_X, END_Y]
VEL = 10.0
EPSILON = 0.1


def inflate_square(map, i, j):
    """Inflates a square of a map."""
    try:
        if map[i][j] != 1:
            map[i][j] = 2  # set to two provisionally
    except:
        pass


def inflate_map(map_name):
    """Inflates obstacles in a map to simulate a no volume robot."""
    map = []
    with open(FILE_NAME.format(map_name), "r") as f:  # opening and reading file
        content = f.read()
        for l in content.split("\n"):
            row = []
            for c in l.split(","):
                if c != '':
                    row.append(int(c))
            if row:
                map.append(row)
    f.close()

    for i in range(len(map)):  # inflating
        for j in range(len(map[0])):
            if map[i][j] == 1:
                inflate_square(map, i-1, j)
                inflate_square(map, i, j-1)
                inflate_square(map, i+1, j)
                inflate_square(map, i, j+1)

    for i in range(len(map)):  # renaming inflated squares
        for j in range(len(map[0])):
            if map[i][j] == 2:
                map[i][j] = 1

    with open(FILE_NAME.format(map_name + "_inflated"), "w") as f:  # rewriting in new file
        for i in range(len(map)):
            for j in range(len(map[0])):
                f.write(str(map[i][j]))
                if j != len(map[0]) -1:
                    f.write(",")
            f.write("\n")
    f.close()
    return map_name + "_inflated"


def optimize_route(route):
    """Optimizes a route shortening its length.
        pe: [0, 1] - [1, 1] - [2, 1] == [0, 1] - [2, 1]"""
    redundants = []
    optimized = []

    previous = None
    current = route[0]
    next_ = None
    for i, step in enumerate(route):
        if i == len(route) - 1:
            break
        previous = current
        current = route[i]
        next_ = route[i+1]
        if i == 0:
            continue
        if previous[0] == current[0] == next_[0]:
            redundants.append(current)
        elif previous[1] == current[1] == next_[1]:
            redundants.append(current)

    for step in route:
        if step not in redundants:
            optimized.append(step)

    return optimized


def get_route(map_name, start, end):
    """Execs python file astar.py and returns the route optimized."""
    map_inflated = inflate_map(map_name)  # route on inflated map
    try:
        map = astar.CharMapCost(FILE_NAME.format(map_inflated), start, end)
    except UserInputException:
        print("[Error] Exiting..", file=stderr)
        return -1

    sys.stdout = open(os.devnull, 'w')  # silence
    goalParentId = astar.astar(map)
    route = astar.get_route(map.closed_nodes, goalParentId)
    sys.stdout = sys.__stdout__  # back to standar verbosity

    steps = []
    for node in route:
        steps.append([node.x, node.y])

    return optimize_route(steps)  # the return is an optimized


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
        # print(self.collidelist(self.sim.map.walls))
        if self.collidelist(self.sim.map.walls) == -1:
            self.move_ip(*self.robot.vel)
            x = (self.center[0] - self.sim.cell_width/4.0) / self.sim.cell_width
            y = (self.center[1] - self.sim.cell_height/4.0) / self.sim.cell_height
            self.robot.pos = [x, y]
        else:
            print("collision")
            self.robot.set_vel([0, 0])

class Map:
    """Basic Map."""
    def __init__(self, filename):
        self.cells = genfromtxt(filename, delimiter=',')
        self.columns = self.cells.shape[0]
        self.rows = self.cells.shape[1]

        self.walls = []


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

                wall = pygame.draw.rect(self.screen, self.COLOR_WALL, pygame.Rect(self.cell_width*j, self.cell_height*i, self.cell_width, self.cell_height))
                self.map.walls.append(wall)
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

    def control_robot(self, incrementX, incrementY):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.robot_view.robot.set_vel([-VEL*2, 0])
        if key[pygame.K_RIGHT]:
            self.robot_view.robot.set_vel([VEL*2, 0])
        if key[pygame.K_UP]:
            self.robot_view.robot.set_vel([0, -VEL*2])
        if key[pygame.K_DOWN]:
            self.robot_view.robot.set_vel([0, VEL*2])
        if key[pygame.K_SPACE]:
            self.robot_view.robot.set_vel([0, 0])
        self.update()


def main(sim, robot, map_name, start, end):
    route = get_route(map_name, start, [end[0]-1, end[1]-1])
    route.append(GOAL)
    print(route)

    ref = route.pop(0)
    print("Going to", ref)
    while True:
        velx = robot.pos[0] - ref[1]
        if velx > EPSILON:
            velx = -VEL
        elif velx < -EPSILON:
            velx = VEL
        else:
            velx = 0.0

        vely = robot.pos[1] - ref[0]
        if vely > EPSILON:
            vely = -VEL
        elif vely < -EPSILON:
            vely = VEL
        else:
            vely = 0.0

        robot.set_vel([velx, vely])
        if velx == 0 and vely == 0:
            if len(route) == 0:
                break
            ref = route.pop(0)  # next
            print("Going to", ref)

        # handle events, avoiding gui freeze
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        sim.update()

        print("Robot at", robot.pos)
        time.sleep(RATE)

    print("GOAL REACHED!")
    time.sleep(1)
    print("BYE!")


if __name__ == "__main__":
    # Command line argument parser, try: python3 a-star.py -h
    parser = argparse.ArgumentParser(description="My Simulator.")
    parser.add_argument('-m', '--map', metavar='MAP', dest='map', default=MAP, help='change map folder')
    parser.add_argument('-s', '--start', type=int, nargs=2, metavar='N', dest='start', default=[START_X, START_Y], help='change start point')
    parser.add_argument('-e', '--end', type=int, nargs=2, metavar='N', dest='end', default=[END_X, END_Y], help='change end point')
    parser.add_argument('-i', action='store_true', help='interactive mode')
    args = parser.parse_args()

    map_name = args.map
    start = args.start
    end = args.end

    sim = Simulator()
    map = Map(map_name + ".csv")
    sim.map = map

    robot = Robot([1, 1])
    sim.load_robot(robot)
    time.sleep(1)

    if args.i:
        print("Interactive Mode")
        print("Control de robot with the arrows (space to stop the robot).")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            sim.control_robot(0, 0)
            time.sleep(RATE)
    else:
        main(sim, robot, map_name, start, end)
