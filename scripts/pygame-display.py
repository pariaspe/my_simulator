#!/usr/bin/env python

import pygame
import time
import sys

# Parse CLI arguments
if (len(sys.argv) != 4):
    print("./pygame-display.py map1.csv 2 2")
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

pixelX = SCREEN_WIDTH/nX
pixelY = SCREEN_HEIGHT/nY

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(COLOR_BACKGROUND)

for i, row in enumerate(inFile):
    for j, cell in enumerate(row):

        if cell == 0:
            continue

        pygame.draw.rect(screen, COLOR_WALL, pygame.Rect( pixelX*j, pixelY*i, pixelX, pixelY ))

pygame.draw.rect(screen, COLOR_ROBOT,
                 pygame.Rect( pixelX*initX+pixelX/4.0, pixelY*initY+pixelY/4.0, pixelX/2.0, pixelY/2.0 ))

pygame.display.flip()
time.sleep(10.0)
