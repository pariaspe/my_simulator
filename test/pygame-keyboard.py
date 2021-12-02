#!/usr/bin/env python

import pygame
import time
import sys

# Parse CLI arguments
if (len(sys.argv) != 4):
    print("./pygame-keyboard.py map1.csv 2 2")
    quit()
inFileStr = sys.argv[1]
initX = float(sys.argv[2])
initY = float(sys.argv[3])

from numpy import genfromtxt
inFile = genfromtxt(inFileStr, delimiter=',')
nX = inFile.shape[0]
nY = inFile.shape[1]

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
COLOR_BACKGROUND = (0, 0, 0)
COLOR_WALL = (255, 255, 255)
COLOR_ROBOT = (255, 0, 0)

SIM_PERIOD_MS = 500.0
VELOCITY = 1.0

pixelX = SCREEN_WIDTH/nX
pixelY = SCREEN_HEIGHT/nY

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(COLOR_BACKGROUND)

class SimRender:
    def __init__(self, robotX, robotY):
        for iX in range(nX):
            #print "iX:",iX
            for iY in range(nY):
                #print "* iY:",iY

                #-- Skip box if map indicates a 0
                if inFile[iX][iY] == 0:
                    continue

                pygame.draw.rect(screen, COLOR_WALL,
                                 pygame.Rect( pixelX*iX, pixelY*iY, pixelX, pixelY ))
                self.robot = pygame.draw.rect(screen, COLOR_ROBOT,
                                              pygame.Rect( pixelX*initX+pixelX/4.0, pixelY*initY+pixelY/4.0, pixelX/2.0, pixelY/2.0 ))
        pygame.display.flip()

    def moveRobot(self, incrementX, incrementY):
        pygame.draw.rect(screen, COLOR_BACKGROUND, self.robot)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
           self.robot.move_ip(-VELOCITY, 0)
        if key[pygame.K_RIGHT]:
           self.robot.move_ip(VELOCITY, 0)
        if key[pygame.K_UP]:
           self.robot.move_ip(0, -VELOCITY)
        if key[pygame.K_DOWN]:
           self.robot.move_ip(0, VELOCITY)
        pygame.draw.rect(screen, COLOR_ROBOT, self.robot)
        pygame.display.update()

simRender = SimRender(initX, initY)
clock = pygame.time.Clock()

running = True       
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    simRender.moveRobot(0,pixelY/2.0)

    clock.tick(SIM_PERIOD_MS)

