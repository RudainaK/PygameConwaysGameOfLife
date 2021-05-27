import pygame
import sys
import math
import copy
import random
import time

pygame.init()
screenWidth = 640
screenHeight = 480
GREY = (133, 133, 133)
LIGHTGREY = (179, 179, 179)
WHITE = (255, 255, 255)

win = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Conway's Game of Life")
win.fill(GREY)
pygame.display.update()

# global vars
currState = [[0 for i in range(64)] for j in range(48)]  # 64x48 array for current state
updatedState = [[0 for i1 in range(64)] for j1 in range(48)]  # 64x48 array for updated state
# now because of how I defined these, access is done by [row][col]


def drawboard():
    for i in range(64):
        pygame.draw.line(win, LIGHTGREY, (i * 10, 0), (i * 10, 479), 1)
    for j in range(48):
        pygame.draw.line(win, LIGHTGREY, (0, j * 10), (639, j * 10), 1)  # (x1, y1), (x2, y2)


def drawbox(x1, y1):
    pygame.draw.rect(win, WHITE, [1+x1, 1+y1, 9, 9])


def drawempty(x1, y1):
    pygame.draw.rect(win, GREY, [1+x1, 1+y1, 9, 9])


def updateboardstate():
    neighbors = 0
    global currState
    global updatedState
    for j in range(48):  # for each cell
        for i in range(64):
            for incrY in range(-1, 2):  # count neighbors
                for incrX in range(-1, 2):
                    x = i+incrX
                    y = j+incrY
                    if (x >= 0) and (y >= 0) and (x < 64) and (y < 48):
                        if incrX != incrY:
                            if currState[y][x] == 1:
                                neighbors += 1
                        elif incrX != 0:
                            if currState[y][x] == 1:
                                neighbors += 1
            if currState[j][i] == 0:  # if cell is dead
                if neighbors == 3:
                    updatedState[j][i] = 1
            elif currState[j][i] == 1:  # if cell is alive
                if neighbors < 2 or neighbors > 3:
                    updatedState[j][i] = 0
            neighbors = 0  # reset num of neighbors
    currState = copy.deepcopy(updatedState)


def drawboardstate():
    for j in range(48):
        for i in range(64):
            if currState[j][i] == 1:
                drawbox(i*10, j*10)
            else:
                drawempty(i*10, j*10)


print("Hi, this is a simple recreation of Conway's Game of Life")
print("Here are the controls:")
print("Space for pause")
print("Use the mouse, and left click to select and deselect boxes")
print("Create and initial pattern and then press space to start")


doneInitialPattern = False
print("In editing mode")
while not doneInitialPattern:
    win.fill(GREY)
    drawboard()
    drawboardstate()
    pygame.display.update()
    for event1 in pygame.event.get():
        if event1.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event1.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:  # done editing
                print("Exiting editing mode")
                doneInitialPattern = True  # continue false, end loop
        else:  # otherwise
            if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                x = math.floor(pygame.mouse.get_pos()[0] / 10)
                y = math.floor(pygame.mouse.get_pos()[1] / 10)
                if currState[y][x] == 1:
                    currState[y][x] = 0
                    updatedState[y][x] = 0
                elif currState[y][x] == 0:
                    currState[y][x] = 1
                    updatedState[y][x] = 1
                drawboardstate()
                pygame.display.update()

while True:
    win.fill(GREY)
    drawboard()
    drawboardstate()
    pygame.event.pump()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:  # spacebar pressed once
                print("In editing mode")
                cont = True  # continue is true
                while cont:
                    for event1 in pygame.event.get():
                        if event1.type == pygame.QUIT:
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit()
                        if event1.type == pygame.KEYDOWN:
                            if pygame.key.get_pressed()[pygame.K_SPACE]:  # spacebar pressed a second time
                                print("Exiting editing mode")
                                cont = False  # continue false, end loop
                        else:  # otherwise
                            if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                                x = math.floor(pygame.mouse.get_pos()[0]/10)
                                y = math.floor(pygame.mouse.get_pos()[1]/10)
                                if currState[y][x] == 1:
                                    currState[y][x] = 0
                                    updatedState[y][x] = 0
                                elif currState[y][x] == 0:
                                    currState[y][x] = 1
                                    updatedState[y][x] = 1
                                drawboardstate()
                                pygame.display.update()
    updateboardstate()
    pygame.display.update()
    pygame.time.wait(500)
