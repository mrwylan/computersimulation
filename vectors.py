import numpy as np

"""Some vector operations."""
def magnitude(arrayOrVector):
    """Returns the magnitude of a array or np.array."""
    return np.sqrt(sum([x*x for x in arrayOrVector]))

def normalize(arrayOrVector):
    """Normalizes a given array of np.array."""
    r = magnitude(arrayOrVector)
    return np.array([x/r for x in arrayOrVector])

def combilize(arrayOrVector):
    """Retruns a tuple of the magnitude and the normalized vector."""
    r = magnitude(arrayOrVector)
    return r, np.array([x/r for x in arrayOrVector])

def randomDirection(dimensions):
    """"Returns a unit vector in a random direction."""
    randoms = [np.random.normal() for i in range(dimensions)]
    return normalize(randoms)