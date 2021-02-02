# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:42:50 2021

@author: Immanuel Albrecht
@email: immanuel@perazim.ch
"""

import numpy as np # package import
from random import random  # funktion import
from abc import ABC, abstractmethod # class import, function import
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def randomDirection(dimensions):
    """"Returns a unit vector in a random direction."""
    randoms = [np.random.normal() for i in range(dimensions)]
    r = np.sqrt(sum(x*x for x in randoms))
    return np.array([x/r for x in randoms])


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
        """Returns True if the boundry is violated."""
        pass
    
    @abstractmethod
    def reflect(self, vector):
        """Returns the Vector reflected at the wall."""
        pass


class Wall(Boundry):
    """Implements a boundry of a cuboid volume."""
    def __init__(self, dimension, modifier, position):
        self.dimension = dimension
        self.modifier = modifier
        self.position = position
    
    def check(self, vector):
        if vector[self.dimension] * self.modifier > self.position:
            return True
        return False
    
    def reflect(self, vector):
        newVector = vector
        newVector[self.dimension] = 2 * self.position - newVector[self.dimension]
        return newVector


class Volume(ABC):
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.setBoundries()
    
    @abstractmethod
    def setBoundries(self):
        self.boundries = []
    
    @abstractmethod
    def randomPosition(self):
        """Returns a random position inside the volume."""
        pass
    
    def checkBoundries(self, position):
        """Returns True if a boundry is violated."""
        for boundry in self.boundries:
            if boundry.check(position):
                return True
        return False
    
    def reflectBoundries(self, position):
        """Returns the vector reflected at boundries it violates."""
        newPosition = position
        while self.checkBoundries(newPosition):
            for boundry in self.boundries:
                if boundry.check(position):
                    newPosition = boundry.reflect(position)
        return newPosition


class Cuboid(Volume):
    def __init__(self, vector):
        self.vector = vector
        super().__init__(len(self.vector))
    
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
    """A class to implement the experiment setup. It takes care of the time aspect."""
    def __init__(self, volume, particles, numberOfSimulationSteps):
        self.volume = volume
        self.particles = particles
        self.numberOfSimulationSteps = numberOfSimulationSteps
    
    def runStep(self):
        for paricle in self.particles:
            particle.position = self.volume.reflectBoundries(particle.position + paricle.speed * particle.direction)
    
    def run(self):
        pass
    
    def createCubeExperiment(cubeEdgeLength, numberOfParticles, numberOfDimensions, numberOfSimulationSteps, maxSpeed):
        cubeVector = []
        for i in range(numberOfDimensions):
            cubeVector.append(abs(cubeEdgeLength))
        cube = Cuboid(np.array(cubeVector))
        particles = []
        for i in range(numberOfParticles):
            part = Particle(cube.randomPosition(), maxSpeed * random(), randomDirection(numberOfDimensions))
            part.showState()
            particles.append(part)
        return Experiment(cube, particles, numberOfSimulationSteps)

experiment = Experiment.createCubeExperiment(10000, 10, 2, 100, 20)