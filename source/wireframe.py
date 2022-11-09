# -*- coding: utf-8 -*-

'''
Módulo para wireframes.
'''

from abc import ABC
from enum import Enum
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
    name: str
    color: tuple
    line_width: float
    coord_list: list[Vector]
    object_type: ObjectType

    # Atributos privados
    _transform: Transform

    def __init__(self, coord_list: list, name: str, color: tuple, line_width: float, object_type: ObjectType) -> None:

        super().__init__()
        self.name = name
        self.color = color
        self.line_width = line_width
        self.coord_list = coord_list
        self.object_type = object_type
        self._transform = Transform(self.center(), Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0))

    @property
    def position(self) -> Vector:
        '''
        Retorna a posição.
        '''

        return self._transform.position

    @property
    def scale(self) -> Vector:
        '''
        Retorna a escala.
        '''

        return self._transform.scale

    @property
    def rotation(self) -> Vector:
        '''
        Retorna a escala.
        '''

        return self._transform.rotation

    def center(self) -> Vector:
        '''
        Retorna o centro do objeto.
        '''

        coord_sum = Vector(0.0, 0.0, 0.0)

        for coord in self.coord_list:
            coord_sum += coord

        return coord_sum / len(self.coord_list)

    # Métodos de transformação
    def translate(self, translation: Vector) -> None:
        '''
        Método para transladar o objeto (Transform::translate).
        '''

        self.coord_list = self._transform.translate(translation, self.coord_list)

    def rescale(self, scale: Vector) -> None:
        '''
        Transformação de escala.
        '''

        self.coord_list = self._transform.rescale(scale, self.coord_list)

    def rotate(self, angle: float, anchor: Vector = None) -> None:
        '''
        Transformação de rotação.
        '''

        self.coord_list = self._transform.rotate(angle, self.coord_list, anchor)


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

    @property
    def end(self) -> Vector:
        '''
        Obtém o ponto final.
        '''

        return self.coord_list[1]

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
    def corner_a(self) -> Vector:
        '''
        Retorna a coordenada A.
        '''

        return self.coord_list[0]

    @property
    def corner_b(self) -> Vector:
        '''
        Retorna a coordenada B.
        '''

        return self.coord_list[1]

    @property
    def corner_c(self) -> Vector:
        '''
        Retorna a coordenada C.
        '''

        return self.coord_list[2]


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

        super().__init__(
            [origin, Vector(origin.x, extension.y), extension, Vector(extension.x, origin.y)],
            name, color, line_width, ObjectType.RECTANGLE)

    @property
    def origin(self) -> Vector:
        '''
        Retorna a coordenada da origem.
        '''

        return self.coord_list[0]

    @property
    def corner_a(self) -> Vector:
        '''
        Retorna a coordenada do canto verticalmente alinhado à origem.
        '''

        return self.coord_list[1]

    @property
    def extension(self) -> Vector:
        '''
        Retorna a coordenada da extensão.
        '''

        return self.coord_list[2]

    @property
    def corner_b(self) -> Vector:
        '''
        Retorna a coordenada do canto verticalmente alinhado à extensão.
        '''

        return self.coord_list[3]
