'''
Módulo para conversão de coordenadas.
'''


from source.backend.math.vector import Vector
from source.backend.objects.window import Window


class Conversor():

    '''
    Conversor.
    '''

    @staticmethod
    def world_to_screen(coord: Vector,
                        screen_width: int,
                        screen_height: int,
                        window: Window,
                        viewport_padding: Vector) -> Vector:
        '''
        Converte a coordenada de mundo para uma coordenada de tela.
        '''

        origin = window.normalized_origin - viewport_padding
        extension = window.normalized_extension + viewport_padding

        x_s = ((coord.x - origin.x) / (extension.x - origin.x)) * screen_width
        y_s = (1 - (coord.y - origin.y) / (extension.y - origin.y)) * screen_height

        return Vector(x_s, y_s)

    @staticmethod
    def world_line_to_screen(line: list[Vector, Vector],
                             screen_width: int,
                             screen_height: int,
                             window: Window,
                             viewport_padding: Vector) -> tuple[Vector, Vector]:
        '''
        Converte uma linha no mundo para uma linha na tela.
        '''

        return (Conversor.world_to_screen(line[0],
                                          screen_width,
                                          screen_height,
                                          window,
                                          viewport_padding),
                Conversor.world_to_screen(line[1],
                                          screen_width,
                                          screen_height,
                                          window,
                                          viewport_padding))

    @staticmethod
    def screen_to_world(coord: Vector,
                        screen_width: int,
                        screen_height: int,
                        window: Window,
                        viewport_padding: Vector) -> Vector:
        '''
        Converte a coordenada de tela para uma coordenada de mundo.
        '''

        origin = window.origin - viewport_padding
        extension = window.extension + viewport_padding

        x_w = (coord.x / screen_width) * (extension.x - origin.x) + origin.x
        y_w = (1.0 - (coord.y / screen_height)) * (extension.y - origin.y) + origin.y

        return Vector(x_w, y_w)
