'''
Módulo para wireframes 3D.
'''

import numpy as np

from source.backend.math.vector import Vector
from source.backend.objects.wireframes_2d import Object, ObjectType


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
