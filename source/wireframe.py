# -*- coding: utf-8 -*-

'''
Módulo para wireframes.
'''


from abc import ABC, abstractmethod
from uuid import uuid4
from source.transform import Transform2D


class Object(ABC):

    '''
    Objeto renderizável.
    '''

    transform: Transform2D
    coord_list: list
    identification: str
    name: str
    color: tuple
    line_width: float

    def __init__(self, coord_list: list, name: str, color: tuple, line_width: float) -> None:

        super().__init__()
        self.coord_list = coord_list
        self.transform = Transform2D(coord_list)

        self.identification = str(uuid4())
        self.name = name
        self.color = color
        self.line_width = line_width

    @property
    def identification(self) -> str:
        '''
        Getter do id.
        '''

        return self._identification

    @identification.setter
    def identification(self, value: str) -> None:
        '''
        Setter do id.
        '''

        self._identification = value

    @property
    def name(self) -> str:
        '''
        Getter do nome.
        '''

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        '''
        Setter do nome.
        '''

        self._name = value

    @property
    def color(self) -> tuple:
        '''
        Getter da cor.
        '''

        return self._color

    @color.setter
    def color(self, value: tuple) -> None:
        '''
        Setter da cor.
        '''

        self._color = value

    @property
    def line_width(self) -> float:
        '''
        Getter da grossura da linha.
        '''

        return self._line_width

    @line_width.setter
    def line_width(self, value: float) -> None:
        '''
        Setter da grossura da linha.
        '''

        self._line_width = value

    @property
    def coord_list(self) -> list:
        return self._coord_list
    
    @coord_list.setter
    def coord_list(self, coord_list: list) -> None:
        self._coord_list = coord_list

    def translate(self, translation: tuple) -> None:
        '''
        Método para transladar o objeto (Transform2D::translate).
        '''
        self.coord_list = self.transform.translate((translation[0], translation[1]))

    # --- Esse(s) método(s) não é mais necessário. Adicionei a lista de coordenadas como atributo de Object.
    # --- No construtor de cada tipo de objeto é necessário passar as coordenadas para o super().
    # --- Achei que fazia mais sentido. Na dúvida, não removi os métodos ainda, mas não estão sendo chamados.
    @abstractmethod
    def get_coord_list(self) -> list:
        '''
        Método abstrato que retorna uma lista de coordenadas.
        '''


class Point(Object):

    '''
    Ponto.
    '''

    x: float
    y: float

    def __init__(self, x: int, y: int, name: str = '', color: tuple = (1, 1, 1), line_width: float = 1.0) -> None:

        super().__init__([(x, y)], name, color, line_width)
        self.x = x
        self.y = y

    def get_coord(self) -> tuple:
        '''
        Retorna a posição.
        '''

        return (self.x, self.y)

    def get_coord_list(self) -> list:
        '''
        Retorna as coordenadas para a renderização.
        '''

        return [(self.x, self.y)]

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
        super().__init__([(x1, y1), (x2, y2)], name, color, line_width)
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
