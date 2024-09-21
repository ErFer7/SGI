# -*- coding: utf-8 -*-

'''
Módulo para wireframes.
'''

from enum import Enum

import numpy as np

from source.backend.transform import Transform
from source.backend.vector import Vector


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


class Point(Object):

    '''
    Ponto.
    '''

    def __init__(self, position: Vector, name: str = '', color: tuple = (1.0, 1.0, 1.0)) -> None:
        super().__init__((position,
                          position + Vector(1.0, 0.0)),
                         ((0, 1),),
                         name,
                         color,
                         1.0,
                         ObjectType.POINT,
                         False,
                         False)


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
        super().__init__((position_a, position_b), ((0, 1),), name, color, line_width, ObjectType.LINE, False, False)


class Wireframe2D(Object):

    '''
    Wireframe
    '''

    def __init__(self,
                 coords: tuple[Vector],
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 object_type: ObjectType = ObjectType.POLYGON,
                 fill: bool = False) -> None:
        lines = []

        for i, _ in enumerate(coords):
            if i < len(coords) - 1:
                lines.append((i, i + 1))
            else:
                lines.append((i, 0))

        super().__init__(coords, tuple(lines), name, color, line_width, object_type, fill, True)


class Triangle(Wireframe2D):

    '''
    Triângulo.
    '''

    def __init__(self,
                 position_a: Vector,
                 position_b: Vector,
                 position_c: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 fill: bool = False) -> None:
        super().__init__((position_a, position_b, position_c),
                         name,
                         color,
                         line_width,
                         ObjectType.TRIANGLE,
                         fill)


class Rectangle(Wireframe2D):

    '''
    Retangulo
    '''

    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 fill: bool = False) -> None:
        super().__init__((origin,
                         Vector(origin.x, extension.y, origin.z),
                         extension,
                         Vector(extension.x, origin.y, origin.z)),
                         name,
                         color,
                         line_width,
                         ObjectType.RECTANGLE,
                         fill)


class BezierCurve(Object):

    '''
    Curva de Bezier.
    '''

    def __init__(self,
                 curve_points: tuple[Vector],
                 steps: int,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0) -> None:
        corrected_points = []
        curve_coords = []

        for i in range(0, len(curve_points), 3):
            if i == len(curve_points) - 1:
                break

            corrected_points.append((curve_points[i], curve_points[i + 1], curve_points[i + 2], curve_points[i + 3]))
            curve_coords += self.generate_curve_coords(curve_points[i],
                                                       curve_points[i + 1: i + 3],
                                                       curve_points[i + 3],
                                                       steps)

        lines = []

        for i in range(len(curve_coords) - 1):
            lines.append((i, i + 1))

        super().__init__(curve_coords, tuple(lines), name, color, line_width, ObjectType.BEZIER_CURVE, False, False)

    def generate_curve_coords(self,
                              start: Vector,
                              control_points: tuple[Vector],
                              end: Vector,
                              steps: int) -> tuple[Vector]:
        '''
        Gera a curva de Bezier.
        '''

        bezier_points_x = np.matrix([[start.x], [control_points[0].x], [control_points[1].x], [end.x]])
        bezier_points_y = np.matrix([[start.y], [control_points[0].y], [control_points[1].y], [end.y]])

        bezier_matrix = np.matrix([[-1, 3, -3, 1],
                                   [3, -6, 3, 0],
                                   [-3, 3, 0, 0],
                                   [1, 0, 0, 0]])

        curve = []

        for step in range(steps):

            t = step / steps

            step_matrix = np.matrix([t**3, t**2, t, 1])

            new_x = step_matrix * bezier_matrix * bezier_points_x
            new_y = step_matrix * bezier_matrix * bezier_points_y

            curve.append(Vector(new_x[0, 0], new_y[0, 0], 0.0))

        return tuple(curve)


class SplineCurve(Object):

    '''
    Spline.
    '''

    def __init__(self,
                 spline_points: tuple[Vector],
                 fill: bool,
                 closed: bool,
                 steps: int,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 forward_diff: bool = True) -> None:

        spline_coords = []

        if forward_diff:
            spline_coords = self.generate_spline_coords_fwd(spline_points, steps, closed)
        else:
            spline_coords = self.generate_spline_coords(spline_points, steps, closed)

        lines = []

        for i, _ in enumerate(spline_coords):
            if i < len(spline_coords) - 1:
                lines.append((i, i + 1))
            elif closed:
                lines.append((len(spline_coords) - 1, 0))

        super().__init__(spline_coords, tuple(lines), name, color, line_width, ObjectType.SPLINE_CURVE, fill, closed)

    def generate_spline_coords_fwd(self, points: tuple[Vector], steps: int, closed: bool) -> tuple[Vector]:
        '''
        Gera a curva spline com forward differeces.
        '''

        spline_coords = []

        b_spline_matrix = (1 / 6) * np.matrix([[-1, 3, -3, 1],
                                               [3, -6, 3, 0],
                                               [-3, 0, 3, 0],
                                               [1, 4, 1, 0]])

        delta = 1.0 / steps

        diff_matrix = np.matrix([[0, 0, 0, 1],
                                 [delta**3, delta**2, delta, 0],
                                 [6 * delta**3, 2 * delta**2, 0, 0],
                                 [6 * delta**3, 0, 0, 0]])

        for i, _ in enumerate(points):
            geometry_matrix_x = None
            geometry_matrix_y = None

            if i + 3 < len(points):
                geometry_matrix_x = np.matrix([[points[i].x], [points[i + 1].x], [points[i + 2].x], [points[i + 3].x]])
                geometry_matrix_y = np.matrix([[points[i].y], [points[i + 1].y], [points[i + 2].y], [points[i + 3].y]])
            else:
                if closed:
                    points_len = len(points)
                    index_a = i % points_len
                    index_b = (i + 1) % points_len
                    index_c = (i + 2) % points_len
                    index_d = (i + 3) % points_len

                    geometry_matrix_x = np.matrix([[points[index_a].x],
                                                   [points[index_b].x],
                                                   [points[index_c].x],
                                                   [points[index_d].x]])

                    geometry_matrix_y = np.matrix([[points[index_a].y],
                                                   [points[index_b].y],
                                                   [points[index_c].y],
                                                   [points[index_d].y]])
                else:
                    break

            coeff_matrix_x = b_spline_matrix * geometry_matrix_x
            coeff_matrix_y = b_spline_matrix * geometry_matrix_y

            initial_conditions_matrix_x = diff_matrix * coeff_matrix_x
            initial_conditions_matrix_y = diff_matrix * coeff_matrix_y

            new_x = initial_conditions_matrix_x[0, 0]
            new_y = initial_conditions_matrix_y[0, 0]

            delta_x = initial_conditions_matrix_x[1, 0]
            delta2_x = initial_conditions_matrix_x[2, 0]
            delta3_x = initial_conditions_matrix_x[3, 0]

            delta_y = initial_conditions_matrix_y[1, 0]
            delta2_y = initial_conditions_matrix_y[2, 0]
            delta3_y = initial_conditions_matrix_y[3, 0]

            spline_coords.append(Vector(new_x, new_y, 0.0))

            for _ in range(steps):

                new_x += delta_x
                new_y += delta_y

                delta_x += delta2_x
                delta_y += delta2_y

                delta2_x += delta3_x
                delta2_y += delta3_y

                spline_coords.append(Vector(new_x, new_y, 0.0))

        return tuple(spline_coords)

    def generate_spline_coords(self, points: tuple[Vector], steps: int, closed: bool) -> tuple[Vector]:
        '''
        Gera a curva spline.
        '''

        b_spline_matrix = (1 / 6) * np.matrix([[-1, 3, -3, 1],
                                               [3, -6, 3, 0],
                                               [-3, 0, 3, 0],
                                               [1, 4, 1, 0]])

        spline_coords = []

        for i, _ in enumerate(points):

            geometry_matrix_x = None
            geometry_matrix_y = None

            if i + 3 < len(points):

                geometry_matrix_x = np.matrix([[points[i].x], [points[i + 1].x], [points[i + 2].x], [points[i + 3].x]])
                geometry_matrix_y = np.matrix([[points[i].y], [points[i + 1].y], [points[i + 2].y], [points[i + 3].y]])
            else:

                if closed:
                    points_len = len(points)
                    index_a = i % points_len
                    index_b = (i + 1) % points_len
                    index_c = (i + 2) % points_len
                    index_d = (i + 3) % points_len

                    geometry_matrix_x = np.matrix([[points[index_a].x],
                                                   [points[index_b].x],
                                                   [points[index_c].x],
                                                   [points[index_d].x]])

                    geometry_matrix_y = np.matrix([[points[index_a].y],
                                                   [points[index_b].y],
                                                   [points[index_c].y],
                                                   [points[index_d].y]])
                else:
                    break

            for step in range(steps):

                t = step / steps
                step_matrix = np.matrix([t**3, t**2, t, 1])
                new_x = step_matrix * b_spline_matrix * geometry_matrix_x
                new_y = step_matrix * b_spline_matrix * geometry_matrix_y
                spline_coords.append(Vector(new_x[0, 0], new_y[0, 0], 0.0))

        return tuple(spline_coords)


class Wireframe3D(Object):

    '''
    Wireframe 3D.
    '''

    def __init__(self,
                 coords: tuple[Vector],
                 lines: tuple[tuple[int, int]],
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 object_type: ObjectType = ObjectType.POLYGON3D) -> None:
        super().__init__(coords, lines, name, color, line_width, object_type, False, True)


class Parallelepiped(Wireframe3D):

    '''
    Paralelepípedo.
    '''

    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0) -> None:

        coords = (origin,
                  Vector(origin.x, extension.y),
                  extension,
                  Vector(extension.x, origin.y),
                  origin + Vector(0.0, 0.0, extension.x - origin.x),
                  Vector(origin.x, extension.y, extension.x - origin.x),
                  extension + Vector(0.0, 0.0, extension.x - origin.x),
                  Vector(extension.x, origin.y, extension.x - origin.x))

        lines = ((0, 1),
                 (1, 2),
                 (2, 3),
                 (3, 0),
                 (0, 4),
                 (1, 5),
                 (2, 6),
                 (3, 7),
                 (4, 5),
                 (5, 6),
                 (6, 7),
                 (7, 4))

        super().__init__(coords, lines, name, color, line_width, ObjectType.PARALLELEPIPED)


class Surface(Wireframe3D):

    '''
    Superfície.
    '''

    def __init__(self,
                 points: tuple[Vector],
                 steps: int,
                 name: str = '',
                 color: tuple = (1, 1, 1),
                 line_width: float = 1) -> None:

        coords, lines = self.generate_surface_coords(points, steps)

        super().__init__(coords, lines, name, color, line_width, ObjectType.SURFACE)

    def generate_surface_coords(self,
                                points: tuple[Vector],
                                steps: int) -> tuple[tuple[Vector], tuple[tuple[int, int]]]:
        '''
        Gera uma superfície.
        '''

        b_spline_matrix = (1 / 6) * np.matrix([[-1, 3, -3, 1],
                                               [3, -6, 3, 0],
                                               [-3, 0, 3, 0],
                                               [1, 4, 1, 0]])

        b_spline_matrix_t = b_spline_matrix.getT()

        surface_coords = []
        lines = []

        for i, _ in enumerate(points):

            geometry_matrix_x = None
            geometry_matrix_y = None
            geometry_matrix_z = None

            if i + 15 < len(points):
                geometry_matrix_x = np.matrix([[points[i+j].x for j in range(4)] for i in range(0, len(points), 4)])
                geometry_matrix_y = np.matrix([[points[i+j].y for j in range(4)] for i in range(0, len(points), 4)])
                geometry_matrix_z = np.matrix([[points[i+j].z for j in range(4)] for i in range(0, len(points), 4)])
            else:
                break

            line_index = 0
            fill_curve_a = True
            curve_a = []
            curve_b = []

            for step_s in range(steps):
                s = step_s / steps
                step_matrix_s = np.matrix([s**3, s**2, s, 1])
                for step_t in range(steps):
                    t = step_t / steps
                    step_matrix_t = np.matrix([[t**3], [t**2], [t], [1]])
                    new_x = step_matrix_s * b_spline_matrix * geometry_matrix_x * b_spline_matrix_t * step_matrix_t
                    new_y = step_matrix_s * b_spline_matrix * geometry_matrix_y * b_spline_matrix_t * step_matrix_t
                    new_z = step_matrix_s * b_spline_matrix * geometry_matrix_z * b_spline_matrix_t * step_matrix_t
                    surface_coords.append(Vector(new_x[0, 0], new_y[0, 0], new_z[0, 0]))

                    if line_index + 1 < len(surface_coords):
                        lines.append((line_index, line_index + 1))

                        if fill_curve_a:
                            curve_a.append(line_index)
                        else:
                            curve_b.append(line_index)
                        line_index += 1

                if fill_curve_a:
                    curve_a.append(line_index)
                else:
                    curve_b.append(line_index)

                if len(curve_a) > 0 and len(curve_b) > 0:

                    for index_a, index_b in zip(curve_a, curve_b):
                        lines.append((index_a, index_b))

                    curve_a = curve_b.copy()
                    curve_b.clear()

                line_index += 1
                fill_curve_a = False

        return (tuple(surface_coords), tuple(lines))


class Window(Rectangle):

    '''
    Janela.
    '''

    cop: Vector
    projected_cop: Vector
    projected_position: Vector

    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 cop: Vector,
                 color: tuple = (0.5, 0.0, 0.5),
                 line_width: float = 2.0) -> None:
        super().__init__(origin, extension, 'Window', color, line_width, False)

        self.cop = cop
        self.projected_cop = self.cop
        self.projected_position = self.position

    @property
    def origin(self) -> Vector:
        '''
        Retorna a coordenada da origem.
        '''

        return self.coords[0]

    @property
    def extension(self) -> Vector:
        '''
        Retorna a coordenada da extensão.
        '''

        return self.coords[2]

    @property
    def normalized_origin(self) -> Vector:
        '''
        Retorna a coordenada normalizada da origem.
        '''

        return self.normalized_coords[0]

    @property
    def normalized_extension(self) -> Vector:
        '''
        Retorna a coordenada normalizada da extensão.
        '''

        return self.normalized_coords[2]

    def calculate_x_axis(self) -> Vector:
        '''
        Calcula o eixo x da window.
        '''

        return self.coords[2] - self.coords[1]

    def calculate_y_vector(self) -> Vector:
        '''
        Retorna o vetor que aponta para cima.
        '''

        return self.coords[1] - self.coords[0]

    def calculate_z_vector(self) -> Vector:
        '''
        Retorna o vetor normal da window.
        '''

        return (self.calculate_x_axis() / 2.0).cross_product(self.calculate_y_vector() / 2.0)

    def calculate_x_projected_axis(self) -> Vector:
        '''
        Calcula o eixo x projetado da window.
        '''

        return self.projected_coords[2] - self.projected_coords[1]

    def calculate_y_projected_vector(self) -> Vector:
        '''
        Retorna o vetor projetado que aponta para cima.
        '''

        return self.projected_coords[1] - self.projected_coords[0]

    def calculate_z_projected_vector(self) -> Vector:
        '''
        Retorna o vetor normal projetado da window.
        '''

        return (self.calculate_x_projected_axis() / 2.0).cross_product(self.calculate_y_projected_vector() / 2.0)

    def calculate_cop_distance(self) -> float:
        '''
        Retorna a distância do cop (projetado) até o centro da window.
        '''

        return (self.projected_position - self.projected_cop).magnitude()

    def translate(self, direction: Vector) -> None:
        coords = self._transform.translate(direction, self.coords + [self.cop])
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def rescale(self, scale: Vector) -> None:
        coords = self._transform.rescale(scale, self.coords + [self.cop])
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def rotate(self, rotation: Vector, origin: Vector | None = None) -> None:
        coords = self._transform.rotate(rotation, self.coords + [self.cop], origin)
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def project(self, cop: Vector, normal: Vector, cop_distance) -> None:
        coords = self._transform.project(cop, normal, cop_distance, self.coords + [cop, self.position], True)
        self.projected_coords = coords[:-2]
        self.projected_cop = coords[-2]
        self.projected_position = coords[-1]
