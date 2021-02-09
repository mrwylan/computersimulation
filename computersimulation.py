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

def magnitude(arrayOrVector):
    return np.sqrt(sum([x*x for x in arrayOrVector]))

def normalize(arrayOrVector):
    r = magnitude(arrayOrVector)
    return np.array([x/r for x in arrayOrVector])

def randomDirection(dimensions):
    """"Returns a unit vector in a random direction."""
    randoms = [np.random.normal() for i in range(dimensions)]
    return normalize(randoms)

class Particle():
    """Models the behaviour of a particle."""
    def __init__(self, position, speed, direction, mass):
        self.position = position
        self.speed = speed
        self.direction = direction
        self.mass = mass
    
    def showState(self):
        print(self.position, self.speed, self.direction)
    
    def move(self):
        self.position = self.position + self.speed * self.direction

class Boundry(ABC):
    """An abstract class for what a boundry should do."""
    def __init__(self):
        self.reflectedImpulse = 0
    
    @abstractmethod
    def check(self, vector):
        """Returns True if the boundry is violated."""
        return False
    
    @abstractmethod
    def reflectPosition(self, vector):
        """Returns the Vector reflected at the wall."""
        return vector
    
    @abstractmethod
    def reflectDirection(self, vector):
        """Returns a reflected direction vector."""
        return vector
    
    def reflectParticle(self, particle):
        """Reflects a particle on the boundry."""
        particle.position = self.reflectPosition(particle.position)
        particle.direction = self.reflectDirection(particle.direction)
        self.reflectedImpulse += particle.speed * particle.mass

class Wall(Boundry):
    """Implements a boundry of a cuboid volume."""
    def __init__(self, dimension, modifier, position):
        self.dimension = dimension
        self.modifier = modifier
        self.position = position
        super().__init__()
    
    def check(self, vector):
        if vector[self.dimension] * self.modifier > self.position:
            return True
        return False
    
    def reflectPosition(self, vector):
        newVector = vector
        newVector[self.dimension] = 2 * self.position - newVector[self.dimension]
        return newVector
    
    def reflectDirection(self, vector):
        newVector = vector
        newVector[self.dimension] = -1 * newVector[self.dimension]
        return newVector

class Volume(ABC):
    """An abstract class that coordinates boundries and holds measurements."""
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.setBoundries()
    
    @abstractmethod
    def setBoundries(self):
        self.boundries = []
    
    @abstractmethod
    def getSurfaceArea(self):
        pass
    
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
    
    def reflectParticle(self, particle):
        """Reflects position and direction of a given particle."""
        while self.checkBoundries(particle.position):
            for boundry in self.boundries:
                if boundry.check(particle.position):
                    boundry.reflectParticle(particle)
    
    def totalReflectedImpulse(self):
        return sum([boundry.reflectedImpulse for boundry in self.boundries])

class Cuboid(Volume):
    """A class that implements the abstract volume in a cuboid shape. See that
    it inherits some functions from its parent class. The cuboid spans form the
    origin to the point of its vector 'self.vector', with its edges oriented othogonally."""
    def __init__(self, vector):
        self.vector = vector
        super().__init__(len(self.vector))
    
    def setBoundries(self):
        WALL_LEFT=-1
        WALL_RIGHT=1
        self.boundries = []
        for index in range(self.dimensions):
            self.boundries.append(Wall(index, WALL_LEFT, 0))
            self.boundries.append(Wall(index, WALL_RIGHT, self.vector[index]))
    
    def getSurfaceArea(self):
        array = []
        for boundry in self.boundries:
            area = 1
            for index in range(self.dimensions):
                if index != boundry.dimension:
                    area *= self.vector[index]
            array.append(area)
        return sum(array)
    
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
        self.stepIndex = 0
    
    def getParticlePositions(self):
        """Returns a np.array with the particle position vectors in each row."""
        return np.array([particle.position for particle in self.particles])

    def calculatePressure(self):
        pressure = self.volume.totalReflectedImpulse()/(self.stepIndex * self.volume.getSurfaceArea())
        print(pressure)
        return pressure 
    
    def runStep(self):
        #print(self.stepIndex)
        for particle in self.particles:
            particle.move()
            self.volume.reflectParticle(particle)
            self.stepIndex += 1
            #particle.showState()
    
    def run(self):
        while self.stepIndex < self.numberOfSimulationSteps:
            self.runStep()
    
    def runAnimated2D(self):
        if not self.volume.dimensions == 2:
            print("Please only animate 2D Particles!")
            return 1
        
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.volume.vector[0])
        ax.set_ylim(0, self.volume.vector[1])
        circles, = ax.plot([], [], 'bo', ms=6)

        def animationFunction(i):
            xdata, ydata = np.transpose(self.getParticlePositions())
            self.runStep()
            circles.set_data(xdata, ydata)
            return circles,
        
        animation = FuncAnimation(fig, func=animationFunction, frames=600, interval=10, blit=True)
        plt.show()
    
    def createCubeExperiment(cubeEdgeLength, numberOfParticles, particleMass, numberOfDimensions, numberOfSimulationSteps, maxSpeed):
        cube = Cuboid(np.array([abs(cubeEdgeLength) for i in range(numberOfDimensions)]))
        particles = []
        for i in range(numberOfParticles):
            part = Particle(cube.randomPosition(), maxSpeed * random(), randomDirection(numberOfDimensions), particleMass)
            part.showState()
            particles.append(part)
        return Experiment(cube, particles, numberOfSimulationSteps)
    
    def createGravityCubeExperiment(cubeEdgeLength, numberOfParticles, particleMass, numberOfDimensions, numberOfSimulationSteps, maxSpeed, gravity):
        cube = Cuboid(np.array([abs(cubeEdgeLength) for i in range(numberOfDimensions)]))
        cube.boundries[3].position = cubeEdgeLength * 30
        particles = []
        for i in range(numberOfParticles):
            part = GravityParticle(cube.randomPosition(), maxSpeed * random(), randomDirection(numberOfDimensions), particleMass, gravity)
            part.showState()
            particles.append(part)
        return Experiment(cube, particles, numberOfSimulationSteps)

"""1 simulation step is one microsecond. Let the cube be 1 qubic meter in milimeters. The speeds we expect are around 1000 meters per second, thus 0.001 meters per """

experiment = Experiment.createCubeExperiment(100, 10, 1, 2, 1000, 1)
experiment.runAnimated2D()
experiment.calculatePressure()