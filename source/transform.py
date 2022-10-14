# -*- coding: utf-8 -*-

'''
Módulo para as operações matemáticas.
'''

import numpy as np


class Vector2D():

    '''
    Vetor 2D.
    '''

    x: float
    y: float

    _list: list

    def __init__(self, x: float, y: float) -> None:

        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):

        if isinstance(other, float):
            return Vector2D(self.x / other, self.y / other)
        raise NotImplementedError


class Vector3D(Vector2D):

    '''
    Vetor 3D.
    '''

    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y)
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, value):
        return Vector3D(self.x + value.x, self.y + value.y, self.z + value.z)

    def __sub__(self, value):
        return Vector3D(self.x - value.x, self.y - value.y, self.z - value.z)

    def __mul__(self, other):

        if isinstance(other, float):
            return Vector3D(self.x * other, self.y * other, self.z * other)

        raise NotImplementedError

    def __div__(self, other):

        if isinstance(other, float):
            return Vector3D(self.x / other, self.y / other, self.z / other)

        raise NotImplementedError


class Transform2D():

    '''
    Transformada.
    '''

    # Atributos públicos
    position: Vector2D  # Posição central do objeto
    rotation: float
    scale: list
    t_matrix: np.array  # translation matrix

    def __init__(self, position: Vector2D, rotation: float = 0.0, scale: tuple = (1.0, 1.0)) -> None:

        self.position = position
        self.rotation = rotation
        self.scale = list(scale)
        self.t_matrix = None

    # Transformações
    def translate(self, translation: Vector2D, coord_list: list[Vector2D]) -> list:
        '''
        Translação de um objeto. Retorna uma nova lista de coordenadas.
        '''

        new_coord_list = []
        tx = translation.x
        ty = translation.y
        self.t_matrix = np.asarray([[1, 0, tx],
                                    [0, 1, ty],
                                    [0, 0, 1]])

        # Translação ponto a ponto
        for coord in coord_list:
            new_coord = np.matmul(self.t_matrix, [coord.x, coord.y, 1])
            new_coord_list.append(Vector2D(new_coord[0], new_coord[1]))

        print(new_coord_list)
        return new_coord_list
