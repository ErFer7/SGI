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

    name: str

    def __init__(self, name: str) -> None:

        super().__init__()
        self.name = name

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

    def __init__(self, position: tuple, name: str = '') -> None:

        super().__init__(name)
        self.transform = Transform2D(position)

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

    def __init__(self, start_position: tuple, end_position: tuple, name: str = '') -> None:

        super().__init__(name)
        self.start = Point(start_position)
        self.end = Point(end_position)

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

    def __init__(self, lines: tuple, name: str = '') -> None:

        super().__init__(name)
        self.lines = []

        for line in lines:
            self.lines.append(Line(line[0], line[1]))

    def get_coord_list(self) -> list:
        '''
        Retorna as coordenadas para a renderização.
        '''

        coords = []

        for line in self.lines:
            coords.append(line.get_coord_list())

        return coords
