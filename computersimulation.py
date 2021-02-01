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


class Volume(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def isInside(self, position):
        pass
    
    @abstractmethod
    def randomPosition(self):
        pass


class Cuboid(Volume):
    def __init__(self, x, y, z):
        super().__init__()
        self.vector = np.array([abs(x), abs(y), abs(z)])
        self.volume = abs(x) * abs(y) * abs(z)
        self.dimensions = len(self.vector)
    
    def isInside(self, array):
        for index in range(self.dimensions):
            if array[index] < 0 or self.vector[index] < array[index]:
                return False
        return True
    
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