# -*- coding: utf-8 -*-

'''
Módulo para o vetor.
'''

from math import sqrt, acos
import numpy as np


class Vector():

    '''
    Vetor 3D.
    '''

    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'{self.x:.2f}, {self.y:.2f}, {self.z:.2f}'

    def __str__(self) -> str:
        return f'{self.x:.2f}, {self.y:.2f}, {self.z:.2f}'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        result = None

        if isinstance(other, (float, int)):
            result = Vector(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector):
            magnitude = self.magnitude() * other.magnitude()

            if magnitude > 0.0:
                result = acos(self.dot_product(other) / magnitude)
            else:
                result = 0.0  # Matematicamente indefinido
        else:
            raise NotImplementedError

        return result

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Vector(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError

    def dot_product(self, other) -> float:
        '''
        Produto escalar.
        '''

        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        '''
        Retorna o vetor perpendicular.
        '''

        cross = np.cross([self.x, self.y, self.z], [other.x, other.y, other.z])

        return Vector(cross[0], cross[1], cross[2])

    def magnitude(self) -> float:
        '''
        Retorna a magnitude.
        '''

        return sqrt(self.x**2 + self.y**2 + self.z**2)
