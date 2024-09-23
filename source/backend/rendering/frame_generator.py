'''
Gerador de frame.
'''

from math import degrees
from source.backend.math.vector import Vector
from source.backend.objects.object import Object
from source.backend.objects.window import Window


class FrameGenerator():

    '''
    Classe para a geração de linhas através da projeção, normalização e
    conversão de linhas de índice para linhas de vetores.
    '''

    @staticmethod
    def generate_frame(window: Window, objects: list[Object]) -> None:
        '''
        Gera o frame.
        '''

        FrameGenerator.project(window, objects)
        FrameGenerator.normalize(window, objects)
        FrameGenerator.generate_vector_lines(window, objects)

    @staticmethod
    def project(window: Window, objects: list[Object]) -> None:
        '''
        Gera as linhas de projeção.
        '''

        normal = window.calculate_z_vector()
        cop_distance = window.calculate_cop_distance()

        for obj in objects + [window]:
            obj.project(window.cop, normal, cop_distance)

    @staticmethod
    def normalize(window: Window, objects: list[Object]) -> None:
        '''
        Normaliza as coordenadas.
        '''

        window_up = window.calculate_y_projected_vector()
        rotation = degrees(window_up * Vector(0.0, 1.0, 0.0))

        if window_up.x > 0.0:
            rotation = 360 - rotation

        for obj in objects:
            obj.normalize(window.position, window.scale, rotation)

    @staticmethod
    def generate_vector_lines(window: Window, objects: list[Object]) -> None:
        '''
        Gera as linhas dos vetores.
        '''

        for obj in objects + [window]:
            obj.generate_vector_lines()
