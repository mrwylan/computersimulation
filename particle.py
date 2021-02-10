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