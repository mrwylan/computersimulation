# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:42:50 2021

@author: Immanuel
"""

import numpy as np # package import
from random import random # funktion import
from abc import ABC, abstractmethod # class import, function import


def randomDirection():
    """
    Returns
    -------
    np.array
        Returns a randomly oriented unit vector.
    """
    phi = np.pi * 2. * random()
    theta = np.pi * random()
    x = np.cos(phi) * np.sin(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(theta)        
    return np.array([x, y, z])


class Particle():
    def __init__(self, position, speed, direction):
        self.positition = position
        self.speed = speed
        self.direction = direction
    
    def showState(self):
        print(self.postition, self.speed, self.direction)


class Volume(ABC):
    def __init__(self):
        self.volume
    
    @abstractmethod
    def isInside(self, vector):
        pass
    
    @abstractmethod
    def randomPosition(self):
        pass


class Cuboid(Volume):
    def __init__(self, x, y, z):
        super().__init__()
        self.size = np.array([x, y, z])
        self.volume = x * y * z
    
    def isInside(self, vector):
        if vector.dimensions != self.size.dimensions:
            print("ERROR: Dimensions didn't match!")
            return
        for index in range(vector.dimensions):
            if vector.array[index] < 0 or self.size.array[index] < vector.array[index]:
                return False
        return True
    
    
        