# -*- coding: utf-8 -*-

'''
Módulo para wireframes.
'''

from abc import ABC
from enum import Enum
from uuid import uuid4
from source.transform import Transform, Vector


class ObjectType(Enum):

    '''
    Tipos de objeto.
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
    coord_list: list[Vector]
    object_type: ObjectType

    # Atributos privados
    _transform: Transform

    def __init__(self, coord_list: list, name: str, color: tuple, line_width: float, object_type: ObjectType) -> None:

        super().__init__()
        self.identification = str(uuid4())
        self.name = name
        self.color = color
        self.line_width = line_width
        self.coord_list = coord_list
        self.object_type = object_type

        coord_sum = Vector(0.0, 0.0, 0.0)

        for coord in self.coord_list:
            coord_sum += coord

        self._transform = Transform(coord_sum / len(self.coord_list))

    @property
    def position(self) -> Vector:
        '''
        Retorna a posição
        '''

        return self._transform.position

    # Métodos de transformação
    def move_to(self, position: Vector) -> None:
        '''
        Move para a posição especificada.
        '''

        self.coord_list = self._transform.move_to(position, self.coord_list)

    def translate(self, translation: Vector) -> None:
        '''
        Método para transladar o objeto (Transform::translate).
        '''

        self.coord_list = self._transform.translate(translation, self.coord_list)

    def scale(self, scale: Vector) -> None:
        '''
        Transformação de escala.
        '''

        self.coord_list = self._transform.scale(scale, self.coord_list)


class Point(Object):

    '''
    Ponto.
    '''

    def __init__(self, position: Vector, name: str = '', color: tuple = (1.0, 1.0, 1.0)) -> None:

        super().__init__([position], name, color, 1.0, ObjectType.POINT)

    # Métodos utilitários
    @property
    def coord(self) -> Vector:
        '''
        Retorna a posição.
        '''

        return self.coord_list[0]

    @coord.setter
    def coord(self, value: Vector) -> None:
        '''
        Define a posição.
        '''

        self.coord_list[0] = value


class Line(Object):

    '''
    Linha.
    '''

    def __init__(self,
                 position_a: Vector,
                 position_b: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0) -> None:

        super().__init__([position_a, position_b], name, color, line_width, ObjectType.LINE)

    # Métodos utilitários
    @property
    def start(self) -> Vector:
        '''
        Obtém o ponto inicial.
        '''

        return self.coord_list[0]

    @start.setter
    def start(self, value: Vector) -> None:
        '''
        Define o ponto inicial.
        '''

        self.coord_list[0] = value

    @property
    def end(self) -> Vector:
        '''
        Obtém o ponto final.
        '''

        return self.coord_list[1]

    @end.setter
    def end(self, value: Vector) -> None:
        '''
        Define o ponto final.
        '''

        self.coord_list[1] = value


class Wireframe(Object):

    '''
    Wireframe
    '''

    def __init__(self,
                 coords: list[Vector],
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 object_type: ObjectType = ObjectType.POLYGON) -> None:

        super().__init__(coords, name, color, line_width, object_type)


class Triangle(Wireframe):

    '''
    Triângulo.
    '''

    def __init__(self,
                 position_a: Vector,
                 position_b: Vector,
                 position_c: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0) -> None:

        super().__init__([position_a, position_b, position_c], name, color, line_width, ObjectType.TRIANGLE)

    @property
    def top(self) -> Vector:
        '''
        Retorna a coordenada B.
        '''

        return self.coord_list[1]

    @top.setter
    def top(self, value: Vector) -> None:
        '''
        Define a coordenada B.
        '''

        self.coord_list[1] = value

    @property
    def left(self) -> Vector:
        '''
        Retorna a coordenada A.
        '''

        return self.coord_list[0]

    @left.setter
    def left(self, value: Vector) -> None:
        '''
        Define a coordenada A.
        '''

        self.coord_list[0] = value

    @property
    def right(self) -> Vector:
        '''
        Retorna a coordenada C.
        '''

        return self.coord_list[2]

    @right.setter
    def right(self, value: Vector) -> None:
        '''
        Define a coordenada C.
        '''

        self.coord_list[2] = value


class Rectangle(Wireframe):

    '''
    Retangulo
    '''

    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0) -> None:

        # TL, BL, BR, TR
        super().__init__(
            [origin, Vector(origin.x, extension.y), extension, Vector(extension.x, origin.y)],
            name, color, line_width, ObjectType.RECTANGLE)

    @property
    def top_left(self) -> Vector:
        '''
        Retorna a coordenada superior esquerda.
        '''

        return self.coord_list[0]

    @top_left.setter
    def top_left(self, value: Vector) -> None:
        '''
        Define a coordenada superior esquerda.
        '''

        self.coord_list[0] = value
        self.coord_list[1].x = value.x
        self.coord_list[3].y = value.y

    @property
    def bottom_left(self) -> Vector:
        '''
        Retorna a coordenada inferior esquerda.
        '''

        return self.coord_list[1]

    @bottom_left.setter
    def bottom_left(self, value: Vector) -> None:
        '''
        Define a coordenada inferior esquerda.
        '''

        self.coord_list[1] = value
        self.coord_list[0].x = value.x
        self.coord_list[2].y = value.y

    @property
    def bottom_right(self) -> Vector:
        '''
        Retorna a coordenada inferior direita.
        '''

        return self.coord_list[2]

    @bottom_right.setter
    def bottom_right(self, value: Vector) -> None:
        '''
        Define a coordenada inferior direita.
        '''

        self.coord_list[2] = value
        self.coord_list[3].x = value.x
        self.coord_list[1].y = value.y

    @property
    def top_right(self) -> Vector:
        '''
        Retorna a coordenada superior direita.
        '''

        return self.coord_list[3]

    @top_right.setter
    def top_right(self, value: Vector) -> None:
        '''
        Define a coordenada superior direita.
        '''

        self.coord_list[3] = value
        self.coord_list[2].x = value.x
        self.coord_list[0].y = value.y
