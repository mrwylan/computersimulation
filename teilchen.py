# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 13:33:49 2021

@author: Jakob
@contrubution: Immanuel
"""
import numpy as np # package import
from random import random # funktion import

class Position:
    def __init__(self, x, y, z):
        self.vektor = np.array([x,y,z])
        
    def getVektor(self):
        return self.vektor
    
    def randomDirection():
        phi = np.pi * 2. * random()
        theta = np.pi * random()
        x = np.cos(phi) * np.sin(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(theta)        
        return Position(x,y,z)


class Teilchen:
    def __init__(self, pos, speed, direction):
        self.position = pos
        self.speed = speed
        self.direction = direction
        
    def showState(self):
        print(self.position.vektor, self.speed, self.direction.vektor)
    
        
class Cube:
    def __init__(self, x, y, z):
        self.size = np.array([x,y,z])
    
    def randomPosition(self):
        return Position(self.randomDim(0), self.randomDim(1), self.randomDim(2))
    
    def randomDim(self, dimension):
        return self.size[dimension] * random()


class Experiment:
    def __init__(self, cube, particles, steps, resolution):
        self.cube = cube
        self.particles = particles
        self.steps = steps       
    
    def runStep(self):
        for particle in self.particles:
            newPostition = particle.position.vector + particle.speed * particle.direction.vektor
            particle.showState()
            
    
    def run(self):
        print("we are ready to run")
        # TODO : move the particle for steps
    
    def create(borderLength, numberOfParicles, numberOfSimulationSteps, maxSpeed, simulationResolution = 1./200.):
        cube = Cube(borderLength, borderLength, borderLength)
        particles = []
        for i in range(numberOfParicles):
            part = Teilchen(cube.randomPosition(), random() * maxSpeed, Position.randomDirection() )
            part.showState()
            particles.append(part)
        return Experiment(cube, particles, numberOfSimulationSteps, simulationResolution)
    
# Zum starten    
experiment = Experiment.create(1)
experiment.run()

