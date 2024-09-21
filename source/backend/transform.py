# -*- coding: utf-8 -*-

'''
Módulo para as operações matemáticas.
'''

from math import degrees, atan2, sqrt
import numpy as np

from source.backend.vector import Vector
from source.backend.matrix import MatrixBuilder


class Transform():

    '''
    Transformada.
    '''

    _matrix: np.matrix

    def __init__(self, position: Vector) -> None:
        self._matrix = MatrixBuilder.build_translation_matrix(position)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(f'P: {self.position}, R: {self.rotation}, S: {self.scale}')

    @property
    def position(self) -> Vector:
        '''
        Getter da posição.
        '''

        position = self._matrix[0:3, 3]

        return Vector(position[0, 0], position[1, 0], position[2, 0])

    @property
    def rotation(self) -> Vector:
        '''
        Getter da rotação.
        '''

        rotation_matrix = self._matrix[0:3, 0:3]

        scale_x = np.linalg.norm(rotation_matrix[:, 0])
        scale_y = np.linalg.norm(rotation_matrix[:, 1])
        scale_z = np.linalg.norm(rotation_matrix[:, 2])

        normalized_rotation_matrix = np.array([
            [rotation_matrix[0, 0] / scale_x, rotation_matrix[0, 1] / scale_y, rotation_matrix[0, 2] / scale_z],
            [rotation_matrix[1, 0] / scale_x, rotation_matrix[1, 1] / scale_y, rotation_matrix[1, 2] / scale_z],
            [rotation_matrix[2, 0] / scale_x, rotation_matrix[2, 1] / scale_y, rotation_matrix[2, 2] / scale_z]
        ])

        sy = sqrt(normalized_rotation_matrix[0, 0] ** 2 + normalized_rotation_matrix[1, 0] ** 2)

        singular = sy < 1e-6

        if not singular:
            x_angle = atan2(normalized_rotation_matrix[2, 1], normalized_rotation_matrix[2, 2])
            y_angle = atan2(-normalized_rotation_matrix[2, 0], sy)
            z_angle = atan2(normalized_rotation_matrix[1, 0], normalized_rotation_matrix[0, 0])
        else:
            x_angle = atan2(-normalized_rotation_matrix[1, 2], normalized_rotation_matrix[1, 1])
            y_angle = atan2(-normalized_rotation_matrix[2, 0], sy)
            z_angle = 0

        return Vector(degrees(x_angle), degrees(y_angle), degrees(z_angle))

    @property
    def scale(self) -> Vector:
        '''
        Getter da escala.
        '''

        rotation_matrix = self._matrix[0:3, 0:3]

        scale_x = np.linalg.norm(rotation_matrix[:, 0])
        scale_y = np.linalg.norm(rotation_matrix[:, 1])
        scale_z = np.linalg.norm(rotation_matrix[:, 2])

        return Vector(scale_x, scale_y, scale_z)

    def get_translated(self, direction: Vector, coords: list[Vector]) -> list[Vector] | np.matrix:
        '''
        Obtém as coordenadas transladadas de um objeto e também retorna a matriz de translação.
        '''

        translation = MatrixBuilder.build_translation_matrix(direction)

        new_coords = []

        # Translação ponto a ponto
        for coord in coords:
            new_coord = np.matmul(translation, coord.internal_vector_4d)
            new_coords.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coords, translation

    def translate(self, direction: Vector, coords: list[Vector]) -> list[Vector]:
        '''
        Translada um objeto e a transformada retornando uma nova lista de coordenadas.
        '''

        new_coords, translation = self.get_translated(direction, coords)

        self._matrix = translation @ self._matrix

        return new_coords

    def get_rotated(self,
                    rotation: Vector,
                    coords: list[Vector],
                    origin: Vector | None = None) -> list[Vector] | np.matrix:
        '''
        Obtém as coordenadas rotacionadas de um objeto e também retorna a matriz de rotação.
        '''

        if origin is None:
            origin = self.position

        relative_to_origin_translation = MatrixBuilder.build_translation_matrix(-origin)
        rotation = MatrixBuilder.build_rotation_matrix(rotation)
        relative_to_self_translation = MatrixBuilder.build_translation_matrix(origin)

        relative_rotation = relative_to_self_translation * rotation * relative_to_origin_translation

        new_coords = []

        for coord in coords:
            new_coord = np.matmul(relative_rotation, coord.internal_vector_4d)
            new_coords.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coords, relative_rotation

    def rotate(self, rotation: Vector, coords: list[Vector], origin: Vector | None = None) -> list[Vector]:
        '''
        Rotaciona o objeto em relação à um ponto.
        '''

        new_coords, rotation = self.get_rotated(rotation, coords, origin)

        self._matrix = rotation @ self._matrix

        return new_coords

    def get_scaled(self, scale: Vector, coords: list[Vector]) -> list[Vector] | np.matrix:
        '''
        Obtém as coordenadas escaladas de um objeto e também retorna a matriz de escala.
        '''

        relative_to_origin_translation = MatrixBuilder.build_translation_matrix(-self.position)
        inverse_rotation = MatrixBuilder.build_rotation_matrix(-self.rotation)
        scaling = MatrixBuilder.build_scaling_matrix(scale)
        rotation = MatrixBuilder.build_rotation_matrix(self.rotation)
        relative_to_self_translation = MatrixBuilder.build_translation_matrix(self.position)

        relative_scaling = relative_to_self_translation @ \
            rotation @ \
            scaling @ \
            inverse_rotation @ \
            relative_to_origin_translation

        new_coords = []

        # Translação ponto a ponto
        for coord in coords:
            new_coord = np.matmul(relative_scaling, coord.internal_vector_4d)
            new_coords.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coords, relative_scaling

    def rescale(self, scale: Vector, coords: list[Vector]) -> list[Vector]:
        '''
        Transformação de escala.
        '''

        new_coords, scaling = self.get_scaled(scale, coords)

        self._matrix = scaling @ self._matrix

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
