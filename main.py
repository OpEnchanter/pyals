# Import Modules
import pygame, math, sys, random, time

# Constants
winSize = (500, 500)
bgColor = (0,0,0)
cellMaxenergy = 10000

# Variables
points = []
constraints = []
energy = []
organisms = []

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
def createPoint(coordinate = tuple[int], connectedTo = list[int] or None, constraintLen = int, vel = tuple[float]):
    point = {
        "pos": coordinate,
        "vel": vel,
        "energy": cellMaxenergy
    }
    points.append(point)
    if connectedTo is not None:
        for idx in connectedTo:
            constraints.append({
                "0": points.index(point),
                "1": idx,
                "len": constraintLen
            })

def createOrganism(objPt = list[tuple[int]], constraintLens = list[int]):
    connectIdx = len(objPt)-2
    ptListLen = len(points)
    cellIdx = []
    for pt in objPt:
        cellIdx.append(objPt.index(pt)+len(points))
    for pt in objPt:
        connectIdx = ((connectIdx+1)%len(objPt))+ptListLen
        print(connectIdx)
        createPoint(pt, [connectIdx], constraintLens[objPt.index(pt)], (0,0))
    for constraint in constraints:
        print(constraint)
    
    organismData = {
        "cells": cellIdx,
        "objective": {
            "executer": None, # Point index (represents what point is executing this action)
            "type": None, # Objective type
            "data": {}, # Objective Data
            "priority": 0,
            "completed": True
        },
        "asyncObjectives": [], # List of objectives to be run async
    }

    organisms.append(organismData)

class cellAi():
    def getTargetSpeed(location, speed):
        if len(energy) != 0:
            closestEnergyDist = 999999
            closestEnergy = None
            for pt in energy:
                if dist(location, pt) < closestEnergyDist:
                    closestEnergyDist = dist(location, pt)
                    closestEnergy = pt

            print("Locating closest energy")

            return ((closestEnergy[0] - location[0]) * speed, (closestEnergy[1] - location[1]) * speed)
        return (0,0)
    
    def calculateEnergy(cell):
        closestEnergyDist = 999999
        closestEnergy = None
        for pt in energy:
            if dist(cell["pos"], pt) < closestEnergyDist:
                closestEnergyDist = dist(cell["pos"], pt)
                closestEnergy = pt

        if closestEnergyDist < 10:
            energy.remove(closestEnergy)
            cell["energy"] += 2000
            if cell["energy"] > cellMaxenergy:
                cell["energy"] = cellMaxenergy
                
            for organism in organisms:
                if points.index(cell) in organism["cells"]:
                    if organism["objective"]["executer"] == points.index(cell):
                        organism["objective"]["completed"] = True
                        organism["objective"]["priority"] = 0

    def runCellActions():
        for cell in points:
            # Cell Death
            if cell["energy"] <= 0:
                for constraint in constraints:
                    if constraint["0"] == points.index(cell) or constraint["1"] == points.index(cell):
                        print(f"Constraint Removed\n0: {constraint['0']}\n1: {constraint['1']}")
                        constraints.remove(constraint)
                        print(constraints)
                cell["energy"] = 5
                points.pop(points.index(cell))
                return

            # Cell objective update
            if cell["energy"] < 8500:
                # Get closest energy
                closestEnergyDist = 99999
                for pt in energy:
                    if dist(cell["pos"], pt) < closestEnergyDist:
                        closestEnergyDist = dist(cell["pos"], pt)

                priority = closestEnergyDist * 8500-cell["energy"]

                for organism in organisms:
                    if points.index(cell) in organism["cells"]:
                        if priority > organism["objective"]["priority"] and organism["objective"]["completed"]:
                            organism["objective"]["priority"] = priority
                            organism["objective"]["type"] = "food"
                            organism["objective"]["executer"] = points.index(cell)
                            organism["objective"]["data"] = {}
                            organism["objective"]["completed"] = False

                




class organismAi():
    def frameStartOrganismUpdate():
        for organism in organisms:
            organism["objective"]["priority"] = 0
    def updateOrganismObjectives():
        organismObjectiveTypes = ["food"]

        for organism in organisms:
            objectiveType = organism["objective"]["type"]
            if objectiveType in organismObjectiveTypes:
                if objectiveType == "food":
                    # Update velocity based on AI
                    index = organism["objective"]["executer"]
                    if index > len(points)-1:
                        index = len(points)-1
                    pt = points[index]
                    pt["vel"] = cellAi.getTargetSpeed(pt["pos"], 0.01)
            



def updatePointPositions():
    for pt in points:
        pt["pos"] = (pt["pos"][0] + pt["vel"][0], pt["pos"][1] + pt["vel"][1])

    for constraint in constraints:
        a = points[constraint["0"]]["pos"]
        b = points[constraint["1"]]["pos"]

        # Pt B
        vec = (b[0] - a[0], b[1] - a[1]) # Get Vector
        mag = math.sqrt(vec[0]**2 + vec[1]**2) # Get Magnitude
        if mag == 0:
            mag = 1

        vec = (vec[0]/mag, vec[1]/mag) # Normalize Vector

        vec = (vec[0]*constraint["len"], vec[1]*constraint["len"]) # Multiply vector by dist

        pos = (a[0]+vec[0], a[1]+vec[1]) # Calculate new world position for pt "a"

        points[constraint["1"]]["pos"] = pos

def updatePointVelocities():
    # Update point velocities
    for pt in points:
        pt["vel"] = (pt["vel"][0]*0.999, pt["vel"][1]*0.999) # Add resistance

        cellAi.calculateEnergy(pt)

        pt["energy"] -= 1

        cellAi.runCellActions()

def render():
    # Draw Organism
    for constraint in constraints:
        pygame.draw.line(win, (255,255,255), points[constraint["0"]]["pos"], points[constraint["1"]]["pos"], 2)
    for pt in points:
        pygame.draw.circle(win, (255-((pt["energy"]/cellMaxenergy)*255), (pt["energy"]/cellMaxenergy)*255, 0), pt["pos"], 5)

    # Draw energy
    for pt in energy:
        pygame.draw.circle(win, (255, 255, 0), pt, 5)


# Create Points
createOrganism([(250, 250), (100, 250), (175, 350)], [30, 30, 30])


for x in range(50):
    energy.append((random.randint(0, win.get_width()), random.randint(0, win.get_height())))






# Main Loop
while True:
    eventHandler() # Handle frame events

    win.fill(bgColor)

    # Frame Updates
    organismAi.frameStartOrganismUpdate()
    updatePointPositions()
    updatePointVelocities()
    organismAi.updateOrganismObjectives()


    # Frame Draw Functions
    render()

    pygame.display.flip()
