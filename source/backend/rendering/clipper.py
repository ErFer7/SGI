'''
Módulo de clipping.
'''

from enum import Enum
from math import inf

from source.backend.math.vector import Vector
from source.backend.objects.object import Object, ObjectType
from source.backend.objects.window import Window


class LineClippingMethod(Enum):
    '''
    Algoritmos de clipping.
    '''

    COHEN_SUTHERLAND = 1
    LIANG_BARSKY = 2


class Intersection(Enum):
    '''
    Tipos de interseção.
    '''

    NULL = 1
    LEFT = 2
    RIGHT = 3
    TOP = 4
    BOTTOM = 5


class Clipper():

    '''
    Clipper.
    '''

    _method: LineClippingMethod

    def __init__(self) -> None:
        self._clipping_method = LineClippingMethod.LIANG_BARSKY

    @property
    def clipping_method(self) -> LineClippingMethod:
        '''
        Getter do método de clipping.
        '''

        return self._clipping_method

    def toggle_clipping_method(self) -> None:
        '''
        Muda o método de clipping.
        '''

        if self._clipping_method == LineClippingMethod.COHEN_SUTHERLAND:
            self._clipping_method = LineClippingMethod.LIANG_BARSKY
        else:
            self._clipping_method = LineClippingMethod.COHEN_SUTHERLAND

    def clip(self, window: Window, object_: Object) -> list[list[Vector]]:
        '''
        Faz o clipping do objeto.
        '''

        if object_.fill:
            return self.clip_polygon(window, object_)

        return self.clip_lines(window, object_)

    def clip_polygon(self, window: Window, object_: Object) -> list[list[Vector]]:
        '''
        Faz o clipping de um objeto e o converte para a representação em linhas.

        O algoritmo de clipping de polígonos é o Sutherland-Hodgeman.
        '''

        coords = object_.normalized_coords

        clipped_lines = []

        if object_.object_type == ObjectType.POINT and len(coords) > 0:
            if (window.normalized_origin.x <= coords[0].x <= window.normalized_extension.x) and \
               (window.normalized_origin.y <= coords[0].y <= window.normalized_extension.y):
                clipped_lines.append(object_.vector_lines[0])
        else:
            clipped_lines = object_.vector_lines
            clipped_lines_temp = []

            for inter in [Intersection.LEFT, Intersection.RIGHT, Intersection.BOTTOM, Intersection.TOP]:
                for line in clipped_lines:
                    comp_inside = None
                    comp_a = None
                    comp_b = None

                    match inter:
                        case Intersection.LEFT:
                            comp_inside = line[0].x > window.normalized_origin.x and \
                                line[1].x > window.normalized_origin.x
                            comp_a = line[0].x > window.normalized_origin.x
                            comp_b = line[1].x > window.normalized_origin.x
                        case Intersection.RIGHT:
                            comp_inside = line[0].x < window.normalized_extension.x and \
                                line[1].x < window.normalized_extension.x
                            comp_a = line[0].x < window.normalized_extension.x
                            comp_b = line[1].x < window.normalized_extension.x
                        case Intersection.BOTTOM:
                            comp_inside = line[0].y > window.normalized_origin.y and \
                                line[1].y > window.normalized_origin.y
                            comp_a = line[0].y > window.normalized_origin.y
                            comp_b = line[1].y > window.normalized_origin.y
                        case Intersection.TOP:
                            comp_inside = line[0].y < window.normalized_extension.y and \
                                line[1].y < window.normalized_extension.y
                            comp_a = line[0].y < window.normalized_extension.y
                            comp_b = line[1].y < window.normalized_extension.y

                    if comp_inside:
                        clipped_lines_temp.append(line)
                    elif comp_a:
                        intersection = self.intersection(window, line, None, inter, False)
                        clipped_lines_temp.append(intersection)
                    elif comp_b:
                        intersection = self.intersection(window, line, inter, None, False)
                        clipped_lines_temp.append(intersection)

                # Patch de linhas
                if object_.fill:
                    for i, _ in enumerate(clipped_lines_temp):
                        if i < len(clipped_lines_temp) - 1:
                            if clipped_lines_temp[i][1] != clipped_lines_temp[i + 1][0]:
                                clipped_lines_temp.insert(i + 1,
                                                          [clipped_lines_temp[i][1], clipped_lines_temp[i + 1][0]])
                        else:
                            if clipped_lines_temp[i][1] != clipped_lines_temp[0][0]:
                                clipped_lines_temp.append([clipped_lines_temp[i][1], clipped_lines_temp[0][0]])

                clipped_lines = clipped_lines_temp.copy()
                clipped_lines_temp.clear()

        return clipped_lines

    def intersection(self,
                     window: Window,
                     line: list[Vector],
                     inter_a: Intersection,
                     inter_b: Intersection,
                     drop_line: bool = True) -> list[Vector]:
        '''
        Cacula a interseção do vetor com a window.
        '''

        angular_coeff = inf

        if (line[1].x - line[0].x) != 0:
            angular_coeff = (line[1].y - line[0].y) / (line[1].x - line[0].x)

        new_line = []

        for inter, vector in zip([inter_a, inter_b], line):

            new_x = vector.x
            new_y = vector.y

            match inter:
                case Intersection.LEFT:
                    new_x = window.normalized_origin.x
                    new_y = angular_coeff * (window.normalized_origin.x - vector.x) + vector.y

                    if (new_y < window.normalized_origin.y or new_y > window.normalized_extension.y) and drop_line:
                        return []
                case Intersection.RIGHT:
                    new_x = window.normalized_extension.x
                    new_y = angular_coeff * (window.normalized_extension.x - vector.x) + vector.y

                    if (new_y < window.normalized_origin.y or new_y > window.normalized_extension.y) and drop_line:
                        return []
                case Intersection.TOP:
                    new_x = vector.x + (1.0 / angular_coeff) * (window.normalized_extension.y - vector.y)
                    new_y = window.normalized_extension.y

                    if (new_x < window.normalized_origin.x or new_x > window.normalized_extension.x) and drop_line:
                        return []
                case Intersection.BOTTOM:
                    new_x = vector.x + (1.0 / angular_coeff) * (window.normalized_origin.y - vector.y)
                    new_y = window.normalized_origin.y

                    if (new_x < window.normalized_origin.x or new_x > window.normalized_extension.x) and drop_line:
                        return []

            new_line.append(Vector(new_x, new_y))

        return new_line

    def clip_lines(self, window: Window, object_: Object) -> list[list[Vector]]:
        '''
        Faz o clipping das linhas.
        '''

        clipped_lines = []

        if self._clipping_method == LineClippingMethod.COHEN_SUTHERLAND:
            def __clip_line(line):
                return self.cohen_sutherland(window, line)
        elif self._clipping_method == LineClippingMethod.LIANG_BARSKY:
            def __clip_line(line):
                return self.liang_barsky(window, line)

        for line in object_.vector_lines:
            clipped_line = __clip_line(line)

            if len(clipped_line) > 0:
                clipped_lines.append(clipped_line)

        return clipped_lines

    def cohen_sutherland(self, window: Window, line: list[Vector]) -> list[Vector]:
        '''
        Clipping de linha com o algoritmo de Cohen-Shuterland.
        '''

        clipped_line = []
        region_codes = []

        for coord in line:

            region_code = 0b0000
            region_code |= 0b0001 if coord.x < window.normalized_origin.x else 0b0000
            region_code |= 0b0010 if coord.x > window.normalized_extension.x else 0b0000
            region_code |= 0b0100 if coord.y < window.normalized_origin.y else 0b0000
            region_code |= 0b1000 if coord.y > window.normalized_extension.y else 0b0000
            region_codes.append(region_code)

        if region_codes[0] | region_codes[1] == 0b0000:
            clipped_line = line
        elif region_codes[0] & region_codes[1] == 0b0000:

            intersections = []

            for region_code in region_codes:
                match region_code:
                    case 0b0000:
                        intersections.append(Intersection.NULL)
                    case 0b0001:
                        intersections.append(Intersection.LEFT)
                    case 0b0010:
                        intersections.append(Intersection.RIGHT)
                    case 0b1000:
                        intersections.append(Intersection.TOP)
                    case 0b0100:
                        intersections.append(Intersection.BOTTOM)
                    case _:
                        intersections.append(None)

            if intersections[0] is not None and intersections[1] is not None:
                clipped_line = self.intersection(window, line, intersections[0], intersections[1])
            else:

                double_try_intersections = []

                for intersection, region_code in zip(intersections, region_codes):

                    if intersection is None:
                        match region_code:
                            case 0b1001:
                                double_try_intersections.append((Intersection.LEFT, Intersection.TOP))
                            case 0b0101:
                                double_try_intersections.append((Intersection.LEFT, Intersection.BOTTOM))
                            case 0b0110:
                                double_try_intersections.append((Intersection.RIGHT, Intersection.BOTTOM))
                            case 0b1010:
                                double_try_intersections.append((Intersection.RIGHT, Intersection.TOP))
                    else:
                        double_try_intersections.append((intersection, None))

                for try_index in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                    clipped_line = self.intersection(window,
                                                     line,
                                                     double_try_intersections[0][try_index[0]],
                                                     double_try_intersections[1][try_index[1]])

                    if len(clipped_line) > 0:
                        break

        return clipped_line

    def liang_barsky(self, window: Window, line: list[Vector]) -> list[Vector]:
        '''
        Clipping de linha com o algoritmo de Liang-Barsky.
        '''

        p1 = -(line[1].x - line[0].x)
        p2 = -p1
        p3 = -(line[1].y - line[0].y)
        p4 = -p3

        q1 = line[0].x - window.normalized_origin.x
        q2 = window.normalized_extension.x - line[0].x
        q3 = line[0].y - window.normalized_origin.y
        q4 = window.normalized_extension.y - line[0].y

        positives = [1]
        negatives = [0]

        if (p1 == 0 and q1 < 0) or (p2 == 0 and q2 < 0) or (p3 == 0 and q3 < 0) or (p4 == 0 and q4 < 0):
            return []

        if p1 != 0:
            ratio_1 = q1 / p1
            ratio_2 = q2 / p2

            if p1 < 0:
                positives.append(ratio_2)
                negatives.append(ratio_1)
            else:
                positives.append(ratio_1)
                negatives.append(ratio_2)
        if p3 != 0:
            ratio_3 = q3 / p3
            ratio_4 = q4 / p4

            if p3 < 0:
                positives.append(ratio_4)
                negatives.append(ratio_3)
            else:
                positives.append(ratio_3)
                negatives.append(ratio_4)

        max_negative = max(negatives)
        min_positive = min(positives)

        if max_negative > min_positive:
            return []

        new_vector_a = Vector(line[0].x + p2 * max_negative, line[0].y + p4 * max_negative)
        new_vector_b = Vector(line[0].x + p2 * min_positive, line[0].y + p4 * min_positive)

        return [new_vector_a, new_vector_b]
