'''
Objeto.
'''

from enum import Enum

from source.backend.math.transform import Transform
from source.backend.math.vector import Vector


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
    POLYGON3D = 6
    BEZIER_CURVE = 7
    SPLINE_CURVE = 8
    PARALLELEPIPED = 9
    SURFACE = 10


class Object():

    '''
    Objeto renderizável.
    '''

    name: str
    color: tuple
    line_width: float
    fill: bool
    closed: bool
    object_type: ObjectType
    coords: list[Vector]
    normalized_coords: list[Vector]
    projected_coords: list[Vector]
    lines: list[tuple[int, int]]
    vector_lines: list[tuple[Vector, Vector]]

    _transform: Transform

    def __init__(self,
                 coords: tuple[Vector],
                 lines: tuple[tuple[int, int]],
                 name: str,
                 color: tuple,
                 line_width: float,
                 object_type: ObjectType,
                 fill: bool,
                 closed: bool) -> None:

        super().__init__()
        self.name = name
        self.color = color
        self.line_width = line_width
        self.fill = fill
        self.closed = closed
        self.object_type = object_type
        self.coords = list(coords)
        self.normalized_coords = coords
        self.projected_coords = coords
        self._transform = Transform(self.calculate_center())
        self.lines = list(lines)
        self.vector_lines = []

        self.generate_vector_lines()

    @property
    def position(self) -> Vector:
        '''
        Retorna a posição.
        '''

        return self._transform.position

    @property
    def rotation(self) -> Vector:
        '''
        Retorna a escala.
        '''

        return self._transform.rotation

    @property
    def scale(self) -> Vector:
        '''
        Retorna a escala.
        '''

        return self._transform.scale

    def calculate_center(self) -> Vector:
        '''
        Retorna o centro do objeto.
        '''

        coord_sum = Vector(0.0, 0.0, 0.0)

        for coord in self.coords:
            coord_sum += coord

        return coord_sum / len(self.coords)

    # Métodos de transformação
    def translate(self, direction: Vector) -> None:
        '''
        Método para transladar o objeto.
        '''

        self.coords = self._transform.translate(direction, self.coords)

    def rotate(self, rotation: Vector, origin: Vector | None = None) -> None:
        '''
        Transformação de rotação.
        '''

        self.coords = self._transform.rotate(rotation, self.coords, origin)

    def rescale(self, scale: Vector) -> None:
        '''
        Transformação de escala.
        '''

        self.coords = self._transform.rescale(scale, self.coords)

    def normalize(self, window_center: Vector, window_scale: Vector, window_rotation: float) -> None:
        '''
        Normaliza as coordenadas.
        '''

        diff_x = 1.0 / window_scale.x
        diff_y = 1.0 / window_scale.y
        diff_z = 1.0 / window_scale.z

        self.normalized_coords = self._transform.normalize(window_center,
                                                           window_rotation,
                                                           Vector(diff_x, diff_y, diff_z),
                                                           self.projected_coords)

    def project(self, cop: Vector, normal: Vector, cop_distance: float) -> None:
        '''
        Gera as coordenadas de projeção.
        '''

        self.projected_coords = self._transform.project(cop, normal, cop_distance, self.coords)

    def generate_vector_lines(self) -> None:
        '''
        Gera as linhas com vetores.
        '''

        self.vector_lines.clear()

        for line in self.lines:
            try:
                self.vector_lines.append((self.normalized_coords[line[0]], self.normalized_coords[line[1]]))
            except IndexError:
                continue
