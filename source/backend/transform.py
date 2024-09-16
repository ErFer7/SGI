# -*- coding: utf-8 -*-

'''
Módulo para as operações matemáticas.
'''

from math import degrees, acos, atan2
import numpy as np

from source.backend.vector import Vector
from source.backend.matrix import MatrixBuilder


class Transform():

    '''
    Transformada.
    '''

    _position: Vector
    _x_axis: Vector
    _y_axis: Vector
    _z_axis: Vector

    def __init__(self, position: Vector) -> None:
        self._position = position

        self._x_axis = self._position + Vector(1.0, 0.0, 0.0)
        self._y_axis = self._position + Vector(0.0, 1.0, 0.0)
        self._z_axis = self._position + Vector(0.0, 0.0, 1.0)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(f'P: {self.position}, R: {self.rotation}, S: {self.scale}')

    @property
    def position(self) -> Vector:
        '''
        Getter da posição.
        '''

        return self._position

    @property
    def rotation(self) -> Vector:
        '''
        Getter da rotação.
        '''

        # TODO: Fix

        local_x_axis = self._x_axis - self._position
        local_y_axis = self._y_axis - self._position
        local_z_axis = self._z_axis - self._position

        local_x_axis.normalize()
        local_y_axis.normalize()
        local_z_axis.normalize()

        # Construct the rotation matrix
        rotation_matrix = np.array([
            [local_x_axis.x, local_y_axis.x, local_z_axis.x],
            [local_x_axis.y, local_y_axis.y, local_z_axis.y],
            [local_x_axis.z, local_y_axis.z, local_z_axis.z]
        ])

        # Decompose the rotation matrix into Euler angles (ZYX order)
        sy = np.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)

        singular = sy < 1e-6

        if not singular:
            x_angle = atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
            y_angle = atan2(-rotation_matrix[2, 0], sy)
            z_angle = atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
        else:
            x_angle = atan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
            y_angle = atan2(-rotation_matrix[2, 0], sy)
            z_angle = 0

        return Vector(degrees(x_angle), degrees(y_angle), degrees(z_angle))

    @property
    def scale(self) -> Vector:
        '''
        Getter da escala.
        '''

        # TODO: Fix

        local_x_axis = self._x_axis - self._position
        local_y_axis = self._y_axis - self._position
        local_z_axis = self._z_axis - self._position

        return Vector(local_x_axis.magnitude(), local_y_axis.magnitude(), local_z_axis.magnitude())

    def get_translated(self, direction: Vector, coords: list[Vector]) -> list[Vector]:
        '''
        Obtém as coordenadas transladadas de um objeto.
        '''

        translation = MatrixBuilder.build_translation_matrix(direction)

        new_coords = []

        # Translação ponto a ponto
        for coord in coords:
            new_coord = np.matmul(translation, coord.internal_vector_4d)
            new_coords.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coords

    def translate(self, direction: Vector, coords: list[Vector]) -> list[Vector]:
        '''
        Translada um objeto e a transformada retornando uma nova lista de coordenadas.
        '''

        self._position += direction
        self._x_axis += direction
        self._y_axis += direction
        self._z_axis += direction

        return self.get_translated(direction, coords)

    def get_rotated(self, rotation: Vector, coords: list[Vector], origin: Vector | None = None) -> list[Vector]:
        '''
        Obtém as coordenadas rotacionadas de um objeto.
        '''

        if origin is None:
            origin = self._position

        relative_to_origin_translation = MatrixBuilder.build_translation_matrix(-origin)
        rotation = MatrixBuilder.build_rotation_matrix(rotation)
        relative_to_self_translation = MatrixBuilder.build_translation_matrix(origin)

        relative_rotation = relative_to_self_translation * rotation * relative_to_origin_translation

        new_coords = []

        for coord in coords:
            new_coord = np.matmul(relative_rotation, coord.internal_vector_4d)
            new_coords.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coords

    def rotate(self, rotation: Vector, coords: list[Vector], origin: Vector | None = None) -> list[Vector]:
        '''
        Rotaciona o objeto em relação à um ponto.
        '''

        internal_coords = self.get_rotated(rotation,
                                           [self._position, self._x_axis, self._y_axis, self._z_axis],
                                           origin)
        new_coords = self.get_rotated(rotation, coords, origin)

        self._position = internal_coords[0]
        self._x_axis = internal_coords[1]
        self._y_axis = internal_coords[2]
        self._z_axis = internal_coords[3]

        return new_coords

    def get_scaled(self, scale: Vector, coords: list[Vector]) -> list[Vector]:
        '''
        Obtém as coordenadas escaladas de um objeto.
        '''

        relative_to_origin_translation = MatrixBuilder.build_translation_matrix(-self._position)
        scaling = MatrixBuilder.build_scaling_matrix(scale)
        relative_to_self_translation = MatrixBuilder.build_translation_matrix(self._position)

        relative_scaling = relative_to_self_translation * scaling * relative_to_origin_translation

        new_coords = []

        # Translação ponto a ponto
        for coord in coords:
            new_coord = np.matmul(relative_scaling, coord.internal_vector_4d)
            new_coords.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coords

    def rescale(self, scale: Vector, coords: list[Vector]) -> list[Vector]:
        '''
        Transformação de escala.
        '''

        internal_coords = self.get_scaled(scale, [self._x_axis, self._y_axis, self._z_axis])
        new_coords = self.get_scaled(scale, coords)

        self._x_axis = internal_coords[0]
        self._y_axis = internal_coords[1]
        self._z_axis = internal_coords[2]

        return new_coords

    def normalize(self,
                  window_position: Vector,
                  window_rotation: float,
                  window_scale: Vector,
                  coords: list[Vector]) -> list[Vector]:
        '''
        Normaliza as coordenadas.
        '''

        normalization = MatrixBuilder.build_normalization_matrix(window_position, window_rotation, window_scale)

        new_coords = []

        for coord in coords:
            new_coord = np.matmul(normalization, coord.internal_vector_4d)
            new_coords.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coords

    def project(self,
                cop: Vector,
                normal: Vector,
                cop_distance: float,
                coords: list[Vector],
                is_window: bool = False) -> list[Vector]:
        '''
        Projeta as coordendas.
        '''

        projection_matrix = MatrixBuilder.build_projection_matrix(cop, normal)
        perspective_matrix = MatrixBuilder.build_perspective_matrix(cop_distance)

        new_coords = []

        for coord in coords:
            new_coord = projection_matrix @ [coord.x, coord.y, coord.z, 1]
            new_vec = Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2])

            if is_window:
                new_coords.append(new_vec)
            else:
                new_coord = perspective_matrix @ new_coord.transpose()

                if new_coord[2, 0] >= 0.0 and new_coord[3, 0] > 0.0:
                    new_vec = Vector(new_coord[0, 0] / new_coord[3, 0],
                                     new_coord[1, 0] / new_coord[3, 0],
                                     new_coord[2, 0] / new_coord[3, 0])
                    new_coords.append(new_vec)

        return new_coords
