# Import Modules
import pygame, math, sys, random

# Constants
winSize = (500, 500)
bgColor = (0,0,0)

# Variables
points = []
constraints = []

# Initialization
pygame.init()
win = pygame.display.set_mode(winSize)

# Functions
def eventHandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def dist(a, b) -> float:
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

def createPoint(coordinate = tuple[int], connectedTo = int or None, constraintLen = int, vel = tuple[float]):
    points.append({
        "pos": coordinate,
        "vel": vel
    })
    if connectedTo is not None:
        constraints.append({
            "0": len(points)-1,
            "1": connectedTo,
            "len": constraintLen
        })

def updatePointPositions():
    for pt in points:
        pt["pos"] = (pt["pos"][0] + pt["vel"][0], pt["pos"][1] + pt["vel"][1])

    for constraint in constraints:
        a = points[constraint["0"]]["pos"]
        b = points[constraint["1"]]["pos"]


        # Pt A
        vec = (a[0] - b[0], a[1] - b[1]) # Get Vector
        mag = math.sqrt(vec[0]**2 + vec[1]**2) # Get Magnitude

        vec = (vec[0]/mag, vec[1]/mag) # Normalize Vector

        vec = (vec[0]*constraint["len"], vec[1]*constraint["len"]) # Multiply vector by dist

        pos = (b[0]+vec[0], b[1]+vec[1]) # Calculate new world position for pt "a"

        points[constraint["0"]]["pos"] = pos

        # Pt B
        vec = (b[0] - a[0], b[1] - a[1]) # Get Vector
        mag = math.sqrt(vec[0]**2 + vec[1]**2) # Get Magnitude

        vec = (vec[0]/mag, vec[1]/mag) # Normalize Vector

        vec = (vec[0]*constraint["len"], vec[1]*constraint["len"]) # Multiply vector by dist

        pos = (a[0]+vec[0], a[1]+vec[1]) # Calculate new world position for pt "a"

        points[constraint["1"]]["pos"] = pos

def updatePointVelocities():
    for pt in points:
        pt["vel"] = (pt["vel"][0]*0.999, pt["vel"][1]*0.999)
    

def render():
    for pt in points:
        pygame.draw.circle(win, (255,255,255), pt["pos"], 5)
    for constraint in constraints:
        pygame.draw.line(win, (255,255,255), points[constraint["0"]]["pos"], points[constraint["1"]]["pos"], 2)


# Create Points
createPoint((250, 250), None, 25, (0.1, 0))
createPoint((100, 250), 0, 25, (0.3, 0.02))

# Main Loop
while True:
    eventHandler() # Handle frame events

    win.fill(bgColor)

    # Frame Updates
    updatePointPositions()
    updatePointVelocities()


    # Frame Draw Functions
    render()

    pygame.display.flip()
