# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from enum import Enum

from source.transform import Vector
from source.wireframe import Window
from source.displayfile import DisplayFileHandler

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class ClippingMethod(Enum):
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


class ViewportHandler():

    '''
    Definição do viewport, este viewport é um handler para um widget DrawingArea.
    '''

    # Atributos privados
    _main_window: None
    _drawing_area: Gtk.DrawingArea
    _bg_color: tuple
    _window: Window
    _drag_coord: Vector
    _viewport_padding: Vector
    _clipping_method: ClippingMethod

    def __init__(self,
                 main_window: DisplayFileHandler,
                 drawing_area: Gtk.DrawingArea,
                 viewport_padding: Vector = Vector(0.0, 0.0, 0.0),
                 bg_color: tuple = (0, 0, 0)) -> None:

        self._main_window = main_window
        self._drawing_area = drawing_area
        self._drawing_area.connect("draw", self.on_draw)
        self._drawing_area.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self._drawing_area.connect("button-press-event", self.on_button_press)
        self._drawing_area.connect("motion-notify-event", self.on_mouse_motion)
        self._drawing_area.connect("button-release-event", self.on_button_release)
        self._drawing_area.connect("scroll-event", self.on_scroll)
        self._drawing_area.connect("size-allocate", self.on_size_allocate)
        self._bg_color = bg_color
        self._window = Window(Vector(-500.0, -500.0), Vector(500.0, 500.0), (0.5, 0.0, 0.5), 2.0)
        self._drag_coord = None
        self._viewport_padding = viewport_padding
        self._clipping_method = ClippingMethod.LIANG_BARSKY

    # Métodos utilitários
    def world_to_screen(self, coord: Vector) -> Vector:
        '''
        Converte a coordenada de mundo para uma coordenada de tela.
        '''

        origin = self._window.normalized_origin - self._viewport_padding
        extension = self._window.normalized_extension + self._viewport_padding

        x_s = ((coord.x - origin.x) / (extension.x - origin.x)) * (self._drawing_area.get_allocated_width())
        y_s = (1 - (coord.y - origin.y) / (extension.y - origin.y)) * self._drawing_area.get_allocated_height()

        return Vector(x_s, y_s)

    def screen_to_world(self, coord: Vector) -> Vector:
        '''
        Converte a coordenada de tela para uma coordenada de mundo.
        '''

        origin = self._window.origin - self._viewport_padding
        extension = self._window.extension + self._viewport_padding

        x_w = (coord.x / self._drawing_area.get_allocated_width()) * (extension.x - origin.x) + origin.x
        y_w = (1.0 - (coord.y / self._drawing_area.get_allocated_height())) * (extension.y - origin.y) + origin.y

        return Vector(x_w, y_w)

    def clip(self, coords: list[Vector]) -> list[Vector]:
        '''
        Faz o clipping de um objeto.

        O algoritmo de clipping de polígonos é o Weiler-Atherton.
        '''

        clipped_coords = []
        coords_size = len(coords)

        if coords_size == 1:
            if (self._window.normalized_origin.x <= coords[0].x <= self._window.normalized_extension.x) and \
               (self._window.normalized_origin.y <= coords[0].y <= self._window.normalized_extension.y):
                clipped_coords.append(Vector(coords[0].x + 1, coords[0].y))
        elif coords_size == 2:

            if self._clipping_method == ClippingMethod.COHEN_SUTHERLAND:
                clipped_coords = self.cohen_sutherland(coords)
            else:
                clipped_coords = self.liang_barsky(coords)
        else:

            # TODO: Arrumar isso aqui

            # Esta é só uma implementação experimental, a implementação oficial será feita depois
            lines = []

            for i, _ in enumerate(coords):
                if i < len(coords) - 1:
                    lines.append([coords[i], coords[i + 1]])

            lines.append([coords[-1], coords[0]])

            clipped_lines = []

            for line in lines:
                if self._clipping_method == ClippingMethod.COHEN_SUTHERLAND:
                    clipped_lines.append(self.cohen_sutherland(line))
                else:
                    clipped_lines.append(self.liang_barsky(line))

            if len(clipped_lines) > 0:

                for line in clipped_lines:

                    if len(line) > 0:
                        clipped_coords.append(line[0])
                        clipped_coords.append(line[1])

        return clipped_coords

    def intersection(self, line: list[Vector], inter_a: Intersection, inter_b: Intersection) -> list[Vector]:
        '''
        Cacula a interseção do vetor com a window.
        '''

        angular_coeff = (line[1].y - line[0].y) / (line[1].x - line[0].x)

        new_line = []

        for inter, vector in zip([inter_a, inter_b], line):

            new_x = vector.x
            new_y = vector.y

            match inter:
                case Intersection.LEFT:
                    new_x = self._window.normalized_origin.x
                    new_y = angular_coeff * (self._window.normalized_origin.x - vector.x) + vector.y

                    if new_y < self._window.normalized_origin.y or new_y > self._window.normalized_extension.y:
                        return []
                case Intersection.RIGHT:
                    new_x = self._window.normalized_extension.x
                    new_y = angular_coeff * (self._window.normalized_extension.x - vector.x) + vector.y

                    if new_y < self._window.normalized_origin.y or new_y > self._window.normalized_extension.y:
                        return []
                case Intersection.TOP:
                    new_x = vector.x + (1.0 / angular_coeff) * (self._window.normalized_extension.y - vector.y)
                    new_y = self._window.normalized_extension.y

                    if new_x < self._window.normalized_origin.x or new_x > self._window.normalized_extension.x:
                        return []
                case Intersection.BOTTOM:
                    new_x = vector.x + (1.0 / angular_coeff) * (self._window.normalized_origin.y - vector.y)
                    new_y = self._window.normalized_origin.y

                    if new_x < self._window.normalized_origin.x or new_x > self._window.normalized_extension.x:
                        return []

            new_line.append(Vector(new_x, new_y))

        return new_line

    def cohen_sutherland(self, line: list[Vector]) -> list[Vector]:
        '''
        Clipping de linha com o algoritmo de Cohen-Shuterland.
        '''

        clipped_line = []
        region_codes = []

        for coord in line:

            region_code = 0b0000
            region_code |= 0b0001 if coord.x < self._window.normalized_origin.x else 0b0000
            region_code |= 0b0010 if coord.x > self._window.normalized_extension.x else 0b0000
            region_code |= 0b0100 if coord.y < self._window.normalized_origin.y else 0b0000
            region_code |= 0b1000 if coord.y > self._window.normalized_extension.y else 0b0000
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
                clipped_line = self.intersection(line, intersections[0], intersections[1])
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
                    clipped_line = self.intersection(line,
                                                     double_try_intersections[0][try_index[0]],
                                                     double_try_intersections[1][try_index[1]])

                    if len(clipped_line) > 0:
                        break

        return clipped_line

    def liang_barsky(self, line: list[Vector]) -> list[Vector]:
        '''
        Clipping de linha com o algoritmo de Liang-Barsky.
        '''

        p1 = -(line[1].x - line[0].x)
        p2 = -p1
        p3 = -(line[1].y - line[0].y)
        p4 = -p3

        q1 = line[0].x - self._window.normalized_origin.x
        q2 = self._window.normalized_extension.x - line[0].x
        q3 = line[0].y - self._window.normalized_origin.y
        q4 = self._window.normalized_extension.y - line[0].y

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

    def coords_to_lines(self, coords: list[Vector]) -> list[tuple]:
        '''
        Converte coordenadas normais para linhas.
        '''

        lines = []

        if len(coords) == 1:
            lines.append((coords[0], Vector(coords[0].x + 1, coords[0].y)))
        else:

            for i, _ in enumerate(coords):
                if i < len(coords) - 1:
                    lines.append((coords[i], coords[i + 1]))

            if len(coords) > 2:
                lines.append((coords[-1], coords[0]))

        return lines

    # Handlers
    def on_draw(self, area, context) -> None:
        '''
        Método para a renderização.
        '''

        # Normaliza os objetos
        self._main_window.display_file_handler.normalize_objects(self._window)

        # Preenche o fundo
        context.set_source_rgb(self._bg_color[0], self._bg_color[1], self._bg_color[2])
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        # Renderiza todos os objetos do display file
        for obj in self._main_window.display_file_handler.objects + [self._window]:

            clipped_coords = self.clip(obj.normalized_coords)
            screen_coords = list(map(self.world_to_screen, clipped_coords))
            lines = self.coords_to_lines(screen_coords)
            color = obj.color
            line_width = obj.line_width

            # Define cor e largura do pincel
            context.new_path()
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)

            for line in lines:

                if obj.fill:
                    context.line_to(line[1].x, line[1].y)
                else:
                    context.move_to(line[0].x, line[0].y)
                    context.line_to(line[1].x, line[1].y)
                    context.stroke()

            context.close_path()

            if obj.fill:
                context.fill()

        self._drawing_area.queue_draw()

    def on_button_press(self, widget, event) -> None:
        '''
        Evento de clique.
        '''

        position = Vector(event.x, event.y)

        if event.button == 1:
            self._main_window.editor_handler.handle_click(self.screen_to_world(position))
        elif event.button == 2:
            self._drag_coord = position

    def on_mouse_motion(self, widget, event):
        '''
        Evento de movimento.
        '''

        if self._drag_coord is not None:

            position = Vector(event.x, event.y)
            diff = self._drag_coord - position
            diff.y = -diff.y
            diff *= self._window.scale.x
            self.move_window(diff)
            self._drag_coord = position

    def on_button_release(self, widget, event) -> None:
        '''
        Evento de liberação do mouse.
        '''

        if event.button == 2:
            self._drag_coord = None

    def on_scroll(self, widget, event) -> None:
        '''
        Evento de rolagem:
        '''

        direction = event.get_scroll_deltas()[2]

        if direction > 0:
            self._window.rescale(Vector(1.03, 1.03, 1.0))
        else:
            self._window.rescale(Vector(0.97, 0.97, 1.0))

        self._main_window.display_file_handler.request_normalization()

    def on_size_allocate(self, allocation, user_data):
        '''
        Evento de alocação.
        '''

        self.reset_window_scale()

        # TODO: Achar maneira melhor de atualizar o tamanho da tela.

        # self._window.rescale(Vector(user_data.width / (self._window.extension.x - self._window.origin.x),
        #                             user_data.height / (self._window.extension.y - self._window.origin.y),
        #                             1.0))

        self._main_window.display_file_handler.request_normalization()

    def move_window(self, direction: Vector) -> None:
        '''
        Move a window.
        '''

        self._window.translate(direction, True)
        self._main_window.display_file_handler.request_normalization()

    def reset_window_position(self) -> None:
        '''
        Redefine a posição da window.
        '''

        self._window.translate(self._window.position * -1)
        self._main_window.display_file_handler.request_normalization()

    def rotate_window(self, angle: float) -> None:
        '''
        Rotaciona a window.
        '''

        self._window.rotate(angle)
        self._main_window.display_file_handler.request_normalization()

    def reset_window_rotation(self) -> None:
        '''
        Redefine a rotação da window.
        '''

        self._window.rotate(-self._window.rotation.z)
        self._main_window.display_file_handler.request_normalization()

    def reescale_window(self, scale: Vector) -> None:
        '''
        Reescala a window.
        '''

        self._window.rescale(scale)
        self._main_window.display_file_handler.request_normalization()

    def reset_window_scale(self) -> None:
        '''
        Redefine a escala da window.
        '''

        diff_x = 1.0 / self._window.scale.x
        diff_y = 1.0 / self._window.scale.y
        diff_z = 1.0 / self._window.scale.z

        self._window.rescale(Vector(diff_x, diff_y, diff_z))
        self._main_window.display_file_handler.request_normalization()
