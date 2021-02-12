import numpy as np
from vectors import magnitude, normalize, combilize

class Particle():
    """Models the behaviour of a particle."""
    def __init__(self, position, speed, direction, mass, radius):
        self.position = position
        self.speed = speed
        self.direction = direction
        self.mass = mass
        self.radius = radius
    
    def showState(self):
        print(self.position, self.speed, self.direction)
    
    def move(self):
        self.position = self.position + self.speed * self.direction
    
    def getImpulseVector(self):
        return self.mass * self.speed * self.direction
    
    def checkCollision(self, particle2):
        """Returns True if the two particles collided."""
        distance = magnitude(self.position - particle2.position)
        if distance < self.radius + particle2.radius and distance > magnitude(self.position + self.direction - particle2.position - particle2.direction):
            return True
        return False

    def collision(self, particle2):
        xrel = particle2.position - self.position
        # We shift the impulse space to give the particle2 zero impulse and save particle 1 in p1.
        impulseShift = particle2.getImpulseVector()
        p1 = self.getImpulseVector() - impulseShift
        p2neu = normalize(xrel) * np.dot(p1, xrel) / magnitude(xrel)
        self.speed, self.direction = combilize((p1 - p2neu + impulseShift) / self.mass)
        particle2.speed, particle2.direction = combilize((p2neu + impulseShift) / particle2.mass)