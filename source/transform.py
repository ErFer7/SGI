# -*- coding: utf-8 -*-

'''
Módulo para as operações matemáticas.
'''

import numpy as np


class Vector():

    '''
    Vetor 3D.
    '''

    x: float
    y: float
    z: float

    _list: list

    def __init__(self, x: float, y: float, z: float = 0.0) -> None:

        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"{self.x:.2f}, {self.y:.2f}, {self.z:.2f}"

    def __str__(self) -> str:
        return f"{self.x:.2f}, {self.y:.2f}, {self.z:.2f}"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):

        if isinstance(other, (float, int)):
            return Vector(self.x * other, self.y * other, self.z * other)
        raise NotImplementedError

    def __truediv__(self, other):

        if isinstance(other, (float, int)):
            return Vector(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError


class Transform():

    '''
    Transformada.
    '''

    # Atributos privados
    _position: Vector
    _rotation: Vector
    _scale: Vector
    _translation_matrix: np.matrix
    _scaling_matrix: np.matrix
    _rotation_matrix: np.matrix

    def __init__(self,
                 position: Vector,
                 rotation: Vector = Vector(0.0, 0.0, 0.0),
                 scale: Vector = Vector(1.0, 1.0, 1.0)) -> None:

        self._position = position
        self._rotation = rotation
        self._scale = scale

        self._translation_matrix = np.matrix([[1.0, 0.0, 0.0, self._position.x],
                                              [0.0, 1.0, 0.0, self._position.y],
                                              [0.0, 0.0, 1.0, self._position.z],
                                              [0.0, 0.0, 0.0, 1.0]])

        self._scaling_matrix = np.matrix([[self._scale.x, 0.0, 0.0, 0.0],
                                          [0.0, self._scale.y, 0.0, 0.0],
                                          [0.0, 0.0, self._scale.z, 0.0],
                                          [0.0, 0.0, 0.0, 1.0]])

        # TODO: Adicionar a matriz de rotação


    def __repr__(self) -> str:
        return str(self._rotation_matrix)

    def __str__(self) -> str:
        return str(self._rotation_matrix)

    @property
    def position(self) -> Vector:
        '''
        Getter da posição.
        '''

        return self._position

    @property
    def scale(self) -> Vector:
        '''
        Getter da escala.
        '''

        return self._scale

    def world_to_local(self, coord: Vector) -> Vector:
        '''
        Calcula o ponto relativo à origem.
        '''

        return coord - self.position

    def local_to_world(self, coord: Vector) -> Vector:
        '''
        Calcula o ponto relativo da coordenada.
        '''

        return coord + self.position

    def move_to(self, position, coord_list) -> list:
        '''
        Move o objeto para a posição.
        '''

        return self.translate(position - self._position, coord_list)

    # Transformações
    def translate(self, direction: Vector, coord_list: list[Vector]) -> list:
        '''
        Translação de um objeto. Retorna uma nova lista de coordenadas.
        '''

        self._position += direction

        self._translation_matrix[0, 3] = direction.x
        self._translation_matrix[1, 3] = direction.y
        self._translation_matrix[2, 3] = direction.z

        new_coord_list = []

        # Translação ponto a ponto
        for coord in coord_list:

            new_coord = np.matmul(self._translation_matrix, [coord.x, coord.y, coord.z, 1])
            new_coord_list.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coord_list

    def rescale(self, scale: Vector, coord_list: list[Vector]) -> list:
        '''
        Transformação de escala.
        '''

        self._scale.x *= scale.x
        self._scale.y *= scale.y
        self._scale.y *= scale.z

        self._scaling_matrix[0, 0] = scale.x
        self._scaling_matrix[1, 1] = scale.y
        self._scaling_matrix[2, 2] = scale.z

        new_coord_list = []

        # Translação ponto a ponto
        for coord in coord_list:

            relative_coord = self.world_to_local(coord)
            new_coord = np.matmul(self._scaling_matrix, [relative_coord.x, relative_coord.y, relative_coord.z, 1])
            relative_new_coord = self.local_to_world(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))
            new_coord_list.append(relative_new_coord)

        return new_coord_list
