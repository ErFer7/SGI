'''
Módulo para as operações matemáticas.
'''

from math import degrees, atan2, sqrt
import numpy as np

from source.backend.math.vector import Vector
from source.backend.math.matrix import Matrix


class Transform():

    '''
    Transformada.
    '''

    _matrix: np.matrix

    def __init__(self, position: Vector) -> None:
        self._matrix = Matrix.build_translation_matrix(position)

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

    def get_translated(self, direction: Vector, coords: list[Vector]) -> tuple[list[Vector], np.matrix]:
        '''
        Obtém as coordenadas transladadas de um objeto e também retorna a matriz de translação.
        '''

        translation = Matrix.build_translation_matrix(direction)

        return Matrix.multiply_vectors(translation, coords), translation

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
                    origin: Vector | None = None) -> tuple[list[Vector], np.matrix]:
        '''
        Obtém as coordenadas rotacionadas de um objeto e também retorna a matriz de rotação.
        '''

        if origin is None:
            origin = self.position

        relative_to_origin_translation = Matrix.build_translation_matrix(-origin)
        rotation = Matrix.build_rotation_matrix(rotation)
        relative_to_self_translation = Matrix.build_translation_matrix(origin)

        relative_rotation = relative_to_self_translation @ rotation @ relative_to_origin_translation

        return Matrix.multiply_vectors(relative_rotation, coords), relative_rotation

    def rotate(self, rotation: Vector, coords: list[Vector], origin: Vector | None = None) -> list[Vector]:
        '''
        Rotaciona o objeto em relação à um ponto.
        '''

        new_coords, rotation = self.get_rotated(rotation, coords, origin)
        self._matrix = rotation @ self._matrix

        return new_coords

    def get_scaled(self, scale: Vector, coords: list[Vector]) -> tuple[list[Vector], np.matrix]:
        '''
        Obtém as coordenadas escaladas de um objeto e também retorna a matriz de escala.
        '''

        relative_to_origin_translation = Matrix.build_translation_matrix(-self.position)
        inverse_rotation = Matrix.build_rotation_matrix(-self.rotation, True)
        scaling = Matrix.build_scaling_matrix(scale)
        rotation = Matrix.build_rotation_matrix(self.rotation)
        relative_to_self_translation = Matrix.build_translation_matrix(self.position)

        relative_scaling = relative_to_self_translation @ \
            rotation @ \
            scaling @ \
            inverse_rotation @ \
            relative_to_origin_translation

        return Matrix.multiply_vectors(relative_scaling, coords), relative_scaling

    def rescale(self, scale: Vector, coords: list[Vector]) -> list[Vector]:
        '''
        Transformação de escala.
        '''

        new_coords, scaling = self.get_scaled(scale, coords)
        self._matrix = scaling @ self._matrix

        return new_coords

    def normalize(self,
                  window_position: Vector,
                  window_z_rotation: float,
                  window_diff_scale: Vector,
                  coords: list[Vector]) -> list[Vector]:
        '''
        Normaliza as coordenadas.
        '''

        normalization = Matrix.build_normalization_matrix(window_position, window_z_rotation, window_diff_scale)

        return Matrix.multiply_vectors(normalization, coords)

    def project(self,
                cop: Vector,
                normal: Vector,
                cop_distance: float,
                coords: list[Vector],
                is_window: bool = False) -> list[Vector]:
        '''
        Projeta as coordendas.
        '''

        if len(coords) == 0:
            return []

        projection_matrix = Matrix.build_projection_matrix(cop, normal)
        perspective_matrix = Matrix.build_perspective_matrix(cop_distance)
        transformation = projection_matrix if is_window else perspective_matrix @ projection_matrix

        internal_vectors = np.stack([coord.internal_vector_4d for coord in coords])
        internal_vectors = np.transpose(internal_vectors)
        transformed_vectors = transformation @ internal_vectors
        tranformed_coords = [Vector(transformed_vectors[0, i], transformed_vectors[1, i], transformed_vectors[2, i])
                             for i in range(transformed_vectors.shape[1])]

        if is_window:
            return tranformed_coords

        new_coords = []

        for i in range(transformed_vectors.shape[1]):
            if transformed_vectors[2, i] >= 0.0 and transformed_vectors[3, i] > 0.0:
                new_coords.append(Vector(transformed_vectors[0, i] / transformed_vectors[3, i],
                                         transformed_vectors[1, i] / transformed_vectors[3, i],
                                         transformed_vectors[2, i] / transformed_vectors[3, i]))

        return new_coords
