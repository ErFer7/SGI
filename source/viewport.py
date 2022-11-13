# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from source.transform import Vector
from source.wireframe import Window
from source.displayfile import DisplayFileHandler
from source.transform import Transform

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


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

    def __init__(self,
                 main_window: DisplayFileHandler,
                 drawing_area: Gtk.DrawingArea,
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
        self._window = Window(Vector(-461.0, -311.5), Vector(461.0, 311.5), (0.5, 0.0, 0.5), 2.0)
        self._drag_coord = None

    # Métodos utilitários
    def world_to_screen(self, coord: Vector) -> Vector:
        '''
        Converte a coordenada de mundo para uma coordenada de tela.
        '''

        origin = self._window.normalized_origin
        extension = self._window.normalized_extension

        x_s = ((coord.x - origin.x) / (extension.x - origin.x)) * self._drawing_area.get_allocated_width()
        y_s = (1 - (coord.y - origin.y) / (extension.y - origin.y)) * self._drawing_area.get_allocated_height()

        return Vector(x_s, y_s)

    def screen_to_world(self, coord: Vector) -> Vector:
        '''
        Converte a coordenada de tela para uma coordenada de mundo.
        '''

        # TODO: Fazer a conversão completa entre tela -> SCN -> mundo

        origin = self._window.origin
        extension = self._window.extension

        x_w = (coord.x / self._drawing_area.get_allocated_width()) * (extension.x - origin.x) + origin.x
        y_w = (1.0 - (coord.y / self._drawing_area.get_allocated_height())) * (extension.y - origin.y) + origin.y

        return Vector(x_w, y_w)

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

            if (len(coords) // 3) % 2 != 0:
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

            screen_coords = list(map(self.world_to_screen, obj.normalized_coords))
            lines = self.coords_to_lines(screen_coords)
            color = obj.color
            line_width = obj.line_width

            # Define cor e largura do pincel
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)


            for line in lines:
                context.move_to(line[0].x, line[0].y)
                context.line_to(line[1].x, line[1].y)
                context.stroke()

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
