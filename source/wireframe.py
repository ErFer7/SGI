# -*- coding: utf-8 -*-

'''
Módulo para wireframes.
'''

from abc import ABC
from uuid import uuid4
from enum import Enum
from source.transform import Transform2D


class ObjectType(Enum):

    '''
    Tipos de objetos
    '''

    NULL = 0
    POINT = 1
    LINE = 2
    TRIANGLE = 3
    RECTANGLE = 4
    POLYGON = 5


class Object(ABC):

    '''
    Objeto renderizável.
    '''

    # Atributos públicos
    identification: str
    name: str
    color: tuple
    line_width: float
    coord_list: list[tuple]
    object_type: ObjectType

    # Atributos privados
    _transform: Transform2D

    def __init__(self, coord_list: list, name: str, color: tuple, line_width: float, object_type: ObjectType) -> None:

        super().__init__()
        self.identification = str(uuid4())
        self.name = name
        self.color = color
        self.line_width = line_width
        self.coord_list = coord_list
        self.object_type = object_type
        self._transform = Transform2D(coord_list)

    # Métodos de transformação
    def translate(self, translation: tuple) -> None:
        '''
        Método para transladar o objeto (Transform2D::translate).
        '''

        self.coord_list = self._transform.translate((translation[0], translation[1]))


class Point(Object):

    '''
    Ponto.
    '''

    def __init__(self, position: tuple, name: str = '', color: tuple = (1, 1, 1)) -> None:

        super().__init__([position], name, color, 1.0, ObjectType.POINT)

    # Métodos utilitários
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

        super().__init__([position_a, position_b], name, color, line_width, ObjectType.LINE)

    # Métodos utilitários
    @property
    def start(self) -> tuple:
        '''
        Obtém o ponto inicial.
        '''

        return self.coord_list[0]

    @start.setter
    def start(self, position: tuple) -> None:
        '''
        Define a posição de início.
        '''

        self.coord_list[0] = position

    @property
    def end(self) -> tuple:
        '''
        Obtém o ponto final.
        '''

        return self.coord_list[1]

    @end.setter
    def end(self, position: tuple) -> None:
        '''
        Define a posição de início.
        '''

        self.coord_list[1] = position


class Wireframe(Object):

    '''
    Wireframe
    '''

    def __init__(self,
                 points: tuple,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1.0,
                 object_type: ObjectType = ObjectType.POLYGON) -> None:

        super().__init__(list(points), name, color, line_width, object_type)


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

        super().__init__([position_a, position_b, position_c], name, color, line_width, ObjectType.TRIANGLE)


class Rectangle(Wireframe):

    '''
    Retangulo
    '''

    def __init__(self,
                 origin: tuple,
                 extension: tuple,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1) -> None:

        super().__init__(
            [origin, (origin[0], extension[1]), extension, (extension[0], origin[1])],
            name, color, line_width, ObjectType.RECTANGLE)
