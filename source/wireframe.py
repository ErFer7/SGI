# -*- coding: utf-8 -*-

'''
Módulo para wireframes.
'''


from abc import ABC, abstractmethod
from source.transform import Transform2D


class Object(ABC):

    '''
    Objeto renderizável.
    '''

    #TODO: setters e getters
    name: str
    color: tuple
    line_width: float

    def __init__(self, name: str, color: tuple, line_width: float) -> None:

        super().__init__()
        self.name = name
        self.color = color
        self.line_width = line_width

    @abstractmethod
    def get_coord_list(self) -> list:
        '''
        Método abstrato que retorna uma lista de coordenadas.
        '''


class Point(Object):

    '''
    Ponto.
    '''

    transform: Transform2D

    def __init__(self, x: int, y: int, name: str = '', color: tuple = (1, 1, 1), line_width: float = 1.0) -> None:

        super().__init__(name, color, line_width)
        self.transform = Transform2D((x, y))

    def get_coord(self) -> list:
        '''
        Retorna a posição.
        '''

        return self.transform.position

    def get_coord_list(self) -> list:
        '''
        Retorna as coordenadas para a renderização.
        '''

        return [self.transform.position, self.transform.position]

class Line(Object):

    '''
    Linha.
    '''

    start: Point
    end: Point

    def __init__(self,
                 x1: int,
                 y1: int,
                 x2: int,
                 y2: int,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1.0) -> None:

        super().__init__(name, color, line_width)
        self.start = Point(x1, y1)
        self.end = Point(x2, y2)

    def get_coord_list(self) -> list:
        '''
        Retorna as coordenadas para a renderização.
        '''

        return [self.start.get_coord(), self.end.get_coord()]

class Wireframe(Object):

    '''
    Wireframe
    '''

    lines: list

    def __init__(self,
                 lines: tuple,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1.0) -> None:

        super().__init__(name, color, line_width)
        self.lines = []

        # Lines: [(x1, y1, x2, y2), ...]

        for line in lines:
            self.lines.append(Line(line[0], line[1], line[2], line[3]))

    def get_coord_list(self) -> list:
        '''
        Retorna as coordenadas para a renderização.
        '''

        coords = []

        for line in self.lines:
            coords.append(line.get_coord_list())

        return coords
