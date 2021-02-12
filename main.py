from typing import List
import numpy as np
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