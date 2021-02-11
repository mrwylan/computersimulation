from typing import List
import numpy as np
from random import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from vectors import randomDirection
import particle
import domain

class Experiment():
    """A class to implement the experiment setup. It takes care of the time aspect."""
    def __init__(self, volume, particles: List[particle.Particle], numberOfSimulationSteps):
        self.volume: domain.Volume = volume
        self.particles = particles
        self.numberOfSimulationSteps = numberOfSimulationSteps
        self.pressure = 0
        self.time: int = 0
    
    def moveParticles(self):
        for part in self.particles:
            part.move()
            self.volume.reflectParticle(part)
    
    def handleParticleCollisions(self):
        for i in range(len(self.particles)):
            for j in np.arange(i, len(self.particles)):
                if i != j and particle.checkCollision(self.particles[i], self.particles[j]):
                    particle.collision(self.particles[i], self.particles[j])
    
    def updatePressure(self):
        impulseHeap = 0
        for boundry in self.volume.boundries:
            impulseHeap += boundry.absorbedImpulse
            boundry.absorbedImpulse = 0
        self.pressure = self.pressure + (impulseHeap / self.volume.surfaceArea - self.pressure) / self.time
    
    def runStep(self):
        self.time += 1
        self.moveParticles()
        self.handleParticleCollisions()
        self.updatePressure()
    
    def run(self):
        for i in np.arange(1, self.numberOfSimulationSteps):
            self.runStep()
    
    def calculateEnergy(self):
        self.energy = 0
        for part in self.particles:
            part.showState()
            self.energy += part.speed * part.speed * part.mass / 2
        print("System energy:", str(self.energy))
        return self.energy
    
    def showPressure(self):
        print("System pressure:", str(self.pressure))
    
    def showState(self):
        self.calculateEnergy()
        self.showPressure()

class Cube2DExperiment(Experiment):
    def __init__(self, volume: domain.Cuboid, particles: List[particle.Particle]):
        super().__init__(volume, particles, 1)
        self.volume: domain.Cuboid = volume
    
    def runAnimated2D(self):
        if not self.volume.dimensions == 2:
            print("Please only animate 2D Particles!")
            return 1
        
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.volume.vector[0])
        ax.set_ylim(0, self.volume.vector[1])
        circles, = ax.plot([], [], 'bo', ms=6)

        def animationFunction(i):
            xdata, ydata = np.transpose([particle.position for particle in self.particles])
            self.runStep()
            circles.set_data(xdata, ydata)
            return circles,
        
        animation = FuncAnimation(fig, func=animationFunction, interval=10, blit=True)
        plt.show()
    
    def createCube2DExperiment(cubeEdgeLength, numberOfParticles, particleMass, maxSpeed, particleRadius):
        NUMBER_OF_DIMENSIONS=2
        cube = domain.Cuboid(np.array([abs(cubeEdgeLength) for i in range(NUMBER_OF_DIMENSIONS)]))
        particles = []
        for i in range(numberOfParticles):
            part = particle.Particle(cube.randomPosition(), maxSpeed * random(), randomDirection(NUMBER_OF_DIMENSIONS), particleMass, particleRadius)
            part.showState()
            particles.append(part)
        return Cube2DExperiment(cube, particles)


exp: Cube2DExperiment = Cube2DExperiment.createCube2DExperiment(100, 100, 1, 1, 1)
exp.showState()
exp.runAnimated2D()
exp.showState()