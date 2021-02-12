from typing import List
import numpy as np
from random import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from vectors import randomDirection
import particle
import domain
from main import Experiment

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