# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from source.transform import Vector
from source.wireframe import Rectangle
from source.displayfile import DisplayFileHandler

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
    _window: Rectangle
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
        self._window = Rectangle(Vector(0.0, 0.0),
                                 Vector(922.0, 623.0),
                                 "Window",
                                 (0.5, 0.0, 0.5),
                                 2.0)
        self._drag_coord = None

    # Métodos utilitários
    def world_to_screen(self, coord: Vector) -> Vector:
        '''
        Converte a coordenada de mundo para uma coordenada de tela.
        '''

        top_left = self._window.top_left
        bottom_right = self._window.bottom_right

        x_s = ((coord.x - top_left.x) / (bottom_right.x - top_left.x)) * self._drawing_area.get_allocated_width()
        y_s = (1 - (coord.y - top_left.y) / (bottom_right.y - top_left.y)) * self._drawing_area.get_allocated_height()

        return Vector(x_s, y_s)

    def screen_to_world(self, coord: Vector) -> Vector:
        '''
        Converte a coordenada de tela para uma coordenada de mundo.
        '''

        top_left = self._window.top_left
        bottom_right = self._window.bottom_right

        x_w = (coord.x / self._drawing_area.get_allocated_width()) * (bottom_right.x - top_left.x) + top_left.x
        y_w = (1 - (coord.y / self._drawing_area.get_allocated_height())) * (bottom_right.y - top_left.y) + top_left.y

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

    def move_window(self, diff: Vector) -> None:
        '''
        Move a janela.
        '''

        self._window.translate(diff)

    # Handlers
    def on_draw(self, area, context) -> None:
        '''
        Método para a renderização.
        '''

        # Preenche o fundo
        context.set_source_rgb(self._bg_color[0], self._bg_color[1], self._bg_color[2])
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        # Renderiza todos os objetos do display file
        for obj in self._main_window.display_file_handler.objects + [self._window]:

            screen_coords = list(map(self.world_to_screen, obj.coord_list))
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

        position = self.screen_to_world(Vector(event.x, event.y))

        if event.button == 1:
            self._main_window.editor_handler.handle_click(position)
        elif event.button == 2:
            self._drag_coord = position

    def on_mouse_motion(self, widget, event):
        '''
        Evento de movimento.
        '''

        position = self.screen_to_world(Vector(event.x, event.y))

        if self._drag_coord is not None:
            self._window.translate(self._drag_coord - position)
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
            self._window.scale(Vector(1.02, 1.02, 1))
        else:
            self._window.scale(Vector(0.98, 0.98, 1))

    def on_size_allocate(self, allocation, user_data):
        '''
        Evento de alocação.
        '''

        # TODO: Corrigir o zoom aqui no futuro
        self._window.bottom_right = Vector(user_data.width, user_data.height)
