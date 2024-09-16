# -*- coding: utf-8 -*-

'''
Módulo para o vetor.
'''

from math import acos
from typing import Union
import numpy as np


class Vector():

    '''
    Vetor 3D.
    '''

    _internal_vector: np.ndarray

    def __init__(self, x: float, y: float, z: float = 0.0, np_vector: np.ndarray = None) -> None:
        self._internal_vector = np_vector.copy() if np_vector is not None else np.array([x, y, z, 1])

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return ', '.join([f'{component: .2f}' for component in self.internal_vector_3d])

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(0.0, 0.0, 0.0, np.add(self._internal_vector, other._internal_vector))

    def __sub__(self, other) -> 'Vector':
        return Vector(0.0, 0.0, 0.0, np.subtract(self._internal_vector, other._internal_vector))

    def __mul__(self, other) -> Union['Vector', float]:
        result = None

        if isinstance(other, (float, int)):  # Escalar
            result = Vector(0.0, 0.0, 0.0, np.multiply(self._internal_vector, other))
        elif isinstance(other, Vector):  # Ângulo entre vetores
            magnitude = self.magnitude() * other.magnitude()

            if magnitude > 0.0:
                result = acos(self.dot(other) / magnitude)
            else:
                result = 0.0  # Matematicamente indefinido
        else:
            raise NotImplementedError

        return result

    def __truediv__(self, other) -> 'Vector':
        if isinstance(other, (float, int)):
            return Vector(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError

    def __neg__(self) -> 'Vector':
        return Vector(0.0, 0.0, 0.0, np.negative(self._internal_vector))

    @property
    def x(self) -> float:
        '''
        Getter de x.
        '''

        return self._internal_vector[0]

    @x.setter
    def x(self, value: float):
        '''
        Setter de x.
        '''

        self._internal_vector[0] = value

    @property
    def y(self) -> float:
        '''
        Getter de y.
        '''

        return self._internal_vector[1]

    @y.setter
    def y(self, value: float):
        '''
        Setter de y.
        '''

        self._internal_vector[1] = value

    @property
    def z(self) -> float:
        '''
        Getter de z.
        '''

        return self._internal_vector[2]

    @z.setter
    def z(self, value: float):
        '''
        Setter de z.
        '''

        self._internal_vector[2] = value

    @property
    def internal_vector_4d(self) -> np.ndarray:
        '''
        Getter do vetor interno.
        '''

        return self._internal_vector

    @property
    def internal_vector_3d(self) -> np.ndarray:
        '''
        Getter do vetor interno.
        '''

        return self._internal_vector[0:3]

    def dot(self, other) -> float:
        '''
        Produto escalar.
        '''

        return np.dot(self.internal_vector_3d, other.internal_vector_3d)

    def cross_product(self, other):
        '''
        Retorna o vetor perpendicular.
        '''

        cross = np.cross(self.internal_vector_3d, other.internal_vector_3d)

        return Vector(cross[0], cross[1], cross[2])

    def magnitude(self) -> float:
        '''
        Retorna a magnitude.
        '''

        return np.sqrt(self.internal_vector_3d.dot(self.internal_vector_3d))

    def normalize(self) -> None:
        '''
        Normaliza o vetor.
        '''

        norm = self.magnitude()
        if norm == 0:
            raise ValueError("Cannot normalize a zero vector")
        self._internal_vector[:3] /= norm
