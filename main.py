# Import Modules
import pygame, math, sys, random

# Constants
winSize = (500, 500)
bgColor = (0,0,0)

# Initialization
pygame.init()
win = pygame.display.set_mode(winSize)

# Functions
def eventHandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Main Loop
while True:
    eventHandler() # Handle frame events

    win.fill(bgColor)

    # Frame Draw Functions

    pygame.display.flip()
