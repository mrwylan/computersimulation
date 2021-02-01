# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:42:50 2021

@author: Immanuel Albrecht
@email: immanuel@perazim.ch
"""

import numpy as np # package import
from random import random, uniform # funktion import
from abc import ABC, abstractmethod # class import, function import


def randomDirection():
    """
    Returns
    -------
    np.array
        Returns a randomly oriented unit vector. See "Spere Point Picking"
    """
    x1 = 1
    x2 = 1
    while x1 * x1 + x2 * x2 >= 1:
        x1 = uniform(-1, 1)
        x2 = uniform(-1, 1)
    x = 2 * x1 * np.sqrt(1 - x1 * x1 - x2 * x2)
    y = 2 * x2 * np.sqrt(1 - x1 * x1 - x2 * x2)
    z = 1 - 2 * (x1 * x1 + x2 * x2)
    return np.array([x, y, z])


class Particle():
    def __init__(self, position, speed, direction):
        self.position = position
        self.speed = speed
        self.direction = direction
    
    def showState(self):
        print(self.position, self.speed, self.direction)


class Boundry(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def check(self, vector):
        pass
    
    @abstractmethod
    def reflect(self, vector):
        pass


class Wall(Boundry):
    def __init__(self, dimension, modifier, position):
        self.dimension = dimension
        self.modifier = modifier
        self.position = position
    
    def check(self, vector):
        """Returns True if the boundry is violated."""
        if vector[self.dimension] * self.modifier > self.position:
            return True
        return False
    
    def reflect(self, vector):
        """Returns the Vector reflected at the wall."""
        newVector = vector
        newVector[self.dimension] = 2 * self.position - newVector[self.dimension]
        return newVector


class Volume(ABC):
    def __init__(self, volume, dimensions):
        self.volume = volume
        self.dimensions = dimensions
        self.setBoundries()
    
    @abstractmethod
    def setBoundries(self):
        self.boundries = []
    
    @abstractmethod
    def randomPosition(self):
        pass
    
    def checkBoundries(self, position):
        """Returns True if a boundry is violated."""
        for boundry in self.boundries:
            if boundry.check(position):
                return True
        return False
    
    def reflectBoundries(self, position):
        newPosition = position
        for boundry in self.boundries:
            if boundry.check(position):
                newPosition = boundry.reflect(position)
        return newPosition


class Cuboid(Volume):
    def __init__(self, x, y, z):
        self.vector = np.array([abs(x), abs(y), abs(z)])
        super().__init__(abs(x) * abs(y) * abs(z), len(self.vector))
    
    def setBoundries(self):
        self.boundries = []
        for index in range(self.dimensions):
            self.boundries.append(Wall(index, -1, 0))
            self.boundries.append(Wall(index, 1, self.vector[index]))
    
    def randomPosition(self):
        array = []
        for index in range(self.dimensions):
            array.append(self.vector[index] * random())
        return np.array(array)


class Experiment():
    def __init__(self, volume, particles, numberOfSimulationSteps):
        self.volume = volume
        self.particles = particles
        self.numberOfSimulationSteps = numberOfSimulationSteps
    
    def runStep(self):
        pass
    
    def run(self):
        print("We are ready to run!")
        self.runStep()
    
    def createCubeExperiment(cubeEdgeLength, numberOfParticles, numberOfSimulationSteps, maxSpeed):
        cube = Cuboid(cubeEdgeLength, cubeEdgeLength, cubeEdgeLength)
        particles = []
        for i in range(numberOfParticles):
            part = Particle(cube.randomPosition(), maxSpeed * random(), randomDirection())
            part.showState()
            particles.append(part)
        return Experiment(cube, particles, numberOfSimulationSteps)

experiment = Experiment.createCubeExperiment(10000, 10, 100, 20)
experiment.run()

for particle in experiment.particles:
    if experiment.volume.checkBoundries(particle.position):
        print("nopedinope")
    else:
        print("huiii")
