'''
Módulo para matrizes.
'''

from math import cos, radians, sin, degrees
import numpy as np

from source.backend.math.vector import Vector


class MatrixBuilder():
    '''
    Classe para construção de matrizes.
    '''

    @staticmethod
    def build_translation_matrix(direction: Vector) -> np.matrix:
        '''
        Constrói a matriz de translação.
        '''

        return np.matrix([[1.0, 0.0, 0.0, direction.x],
                          [0.0, 1.0, 0.0, direction.y],
                          [0.0, 0.0, 1.0, direction.z],
                          [0.0, 0.0, 0.0, 1.0]])

    @staticmethod
    def build_rotation_matrix(rotation: Vector, inverse: bool = False) -> np.matrix:
        '''
        Constrói a matriz de rotação.
        '''

        sinx = sin(radians(rotation.x))
        cosx = cos(radians(rotation.x))
        siny = sin(radians(rotation.y))
        cosy = cos(radians(rotation.y))
        sinz = sin(radians(rotation.z))
        cosz = cos(radians(rotation.z))

        rotation_x = np.matrix([[1.0, 0.0, 0.0, 0.0],
                                [0.0, cosx, -sinx, 0.0],
                                [0.0, sinx, cosx, 0.0],
                                [0.0, 0.0, 0.0, 1.0]])

        rotation_y = np.matrix([[cosy, 0.0, siny, 0.0],
                                [0.0, 1.0, 0.0, 0.0],
                                [-siny, 0.0, cosy, 0.0],
                                [0.0, 0.0, 0.0, 1.0]])

        rotation_z = np.matrix([[cosz, -sinz, 0.0, 0.0],
                                [sinz, cosz, 0.0, 0.0],
                                [0.0, 0.0, 1.0, 0.0],
                                [0.0, 0.0, 0.0, 1.0]])

        if inverse:
            return rotation_x @ rotation_y @ rotation_z

        return rotation_z @ rotation_y @ rotation_x

    @staticmethod
    def build_scaling_matrix(scale: Vector) -> np.matrix:
        '''
        Constrói a matriz de escala.
        '''

        return np.matrix([[scale.x, 0.0, 0.0, 0.0],
                          [0.0, scale.y, 0.0, 0.0],
                          [0.0, 0.0, scale.z, 0.0],
                          [0.0, 0.0, 0.0, 1.0]])

    @staticmethod
    def build_normalization_matrix(window_position: Vector,
                                   window_rotation: float,
                                   window_scale: Vector) -> np.matrix:
        '''
        Constrói a matriz de normalização.
        '''

        translation = MatrixBuilder.build_translation_matrix(-window_position)
        rotation = MatrixBuilder.build_rotation_matrix(Vector(0.0, 0.0, window_rotation))
        scaling = MatrixBuilder.build_scaling_matrix(window_scale)

        return scaling @ rotation @ translation

    @staticmethod
    def build_projection_matrix(cop: Vector, normal: Vector) -> np.matrix:
        '''
        Constrói a matriz de projeção.
        '''

        translation = MatrixBuilder.build_translation_matrix(-cop)
        normal_shadow_xz = Vector(normal.x, 0.0, normal.z)
        rotation_y = degrees(Vector(0.0, 0.0, 1.0) * normal_shadow_xz)

        if normal.x > 0.0:
            rotation_y = 360 - rotation_y

        normal_rotation_matrix = MatrixBuilder.build_rotation_matrix(Vector(0.0, rotation_y, 0.0))
        new_normal = np.matmul(normal_rotation_matrix, normal.internal_vector_4d)
        normal = Vector(new_normal[0, 0], new_normal[0, 1], new_normal[0, 2])

        rotation_x = degrees(Vector(0.0, 0.0, 1.0) * normal)

        if normal.y < 0.0:
            rotation_x = 360 - rotation_x

        rotation_x = MatrixBuilder.build_rotation_matrix(Vector(rotation_x, 0.0, 0.0))
        rotation_y = MatrixBuilder.build_rotation_matrix(Vector(0.0, rotation_y, 0.0))

        return rotation_x @ rotation_y @ translation

    @staticmethod
    def build_perspective_matrix(cop_distance: float) -> np.matrix:
        '''
        Constrói a matriz de perspectiva.
        '''

        return np.matrix([[1.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 1.0 / cop_distance, 0.0]])
