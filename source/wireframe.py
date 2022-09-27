# -*- coding: utf-8 -*-

'''
Módulo para wireframes.
'''


from abc import ABC
from uuid import uuid4
from source.transform import Transform2D


class Object(ABC):

    '''
    Objeto renderizável.
    '''

    identification: str
    name: str
    color: tuple
    line_width: float

    __transform: Transform2D
    __coord_list: list

    def __init__(self, coord_list: list, name: str, color: tuple, line_width: float) -> None:

        super().__init__()
        self.identification = str(uuid4())
        self.name = name
        self.color = color
        self.line_width = line_width

        self.__coord_list = coord_list
        self.__transform = Transform2D(coord_list)

    @property
    def coord_list(self) -> list:
        '''
        Getter da lista de coordenadas.
        '''

        return self.__coord_list

    @coord_list.setter
    def coord_list(self, coord_list: list) -> None:
        '''
        Setter da lista de coordenadas.
        '''

        self.__coord_list = coord_list

    def translate(self, translation: tuple) -> None:
        '''
        Método para transladar o objeto (Transform2D::translate).
        '''

        self.__coord_list = self.__transform.translate((translation[0], translation[1]))


class Point(Object):

    '''
    Ponto.
    '''

    def __init__(self, position: tuple, name: str = '', color: tuple = (1, 1, 1), line_width: float = 1.0) -> None:

        super().__init__([position], name, color, line_width)

    def get_coord(self) -> tuple:
        '''
        Retorna a posição.
        '''

        return self.coord_list[0]


class Line(Object):

    '''
    Linha.
    '''

    def __init__(self,
                 position_a: tuple,
                 position_b: tuple,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1.0) -> None:

        super().__init__([position_a, position_b], name, color, line_width)

    def get_start(self):
        '''
        Obtém o ponto inicial.
        '''

        return self.coord_list[0]

    def get_end(self):
        '''
        Obtém o ponto final.
        '''

        return self.coord_list[1]


class Wireframe(Object):

    '''
    Wireframe
    '''

    def __init__(self,
                 points: tuple,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1.0) -> None:

        super().__init__(list(points), name, color, line_width)

    def get_lines(self) -> list:
        '''
        Retorna as linhas para a renderização.
        '''

        lines = []

        for i, _ in enumerate(self.coord_list):

            if i < len(self.coord_list) - 1:
                lines.append((self.coord_list[i], self.coord_list[i + 1]))

        return lines


class Triangle(Wireframe):

    '''
    Triângulo.
    '''

    def __init__(self,
                 position_a: tuple,
                 position_b: tuple,
                 position_c: tuple,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1) -> None:

        super().__init__([position_a, position_b, position_c], name, color, line_width)


class Rectangle(Wireframe):

    '''
    Retangulo
    '''

    def __init__(self,
                 bottom_left: tuple,
                 bottom_right: tuple,
                 top_left: tuple,
                 top_right: tuple,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1) -> None:

        super().__init__([bottom_left, bottom_right, top_left, top_right], name, color, line_width)
