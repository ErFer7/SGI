# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from source.editor import EditorHandler
from source.transform import Vector2D
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
    _drawing_area: Gtk.DrawingArea
    _display_file: DisplayFileHandler
    _editor: EditorHandler
    _bg_color: tuple
    _window: Rectangle

    def __init__(self,
                 drawing_area: Gtk.DrawingArea,
                 display_file: DisplayFileHandler,
                 editor: EditorHandler,
                 bg_color: tuple = (0, 0, 0)) -> None:

        self._drawing_area = drawing_area
        self._drawing_area.connect("draw", self.on_draw)
        self._drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self._drawing_area.connect("button-press-event", self.on_button_press)
        self._drawing_area.connect("button-release-event", self.on_button_release)
        self._drawing_area.connect("size-allocate", self.on_size_allocate)
        self._display_file = display_file
        self._editor = editor
        self._bg_color = bg_color
        self._window = Rectangle(Vector2D(0.0, 0.0),
                                 Vector2D(922.0, 623.0),
                                 "Window",
                                 (0.5, 0.0, 0.5),
                                 2.0)  # Coordenadas no espaço vetorial do mundo

    # Métodos utilitários
    def world_to_screen(self, coord: Vector2D) -> Vector2D:
        '''
        Converte a coordenada de mundo para uma coordenada de tela.
        '''

        top_left = self._window.top_left
        bottom_right = self._window.bottom_right

        x_s = ((coord.x - top_left.x) / (bottom_right.x - top_left.x)) * self._drawing_area.get_allocated_width()
        y_s = (1 - (coord.y - top_left.y) / (bottom_right.y - top_left.y)) * self._drawing_area.get_allocated_height()

        return Vector2D(x_s, y_s)

    def screen_to_world(self, coord: Vector2D) -> Vector2D:
        '''
        Converte a coordenada de tela para uma coordenada de mundo.
        '''

        top_left = self._window.top_left
        bottom_right = self._window.bottom_right

        x_w = (coord.x / self._drawing_area.get_allocated_width()) * (bottom_right.x - top_left.x) + top_left.x
        y_w = (1 - (coord.y / self._drawing_area.get_allocated_height())) * (bottom_right.y - top_left.y) + top_left.y

        return Vector2D(x_w, y_w)

    def coords_to_lines(self, coords: list[Vector2D]) -> list[tuple]:
        '''
        Converte coordenadas normais para linhas.
        '''

        lines = []

        if len(coords) == 1:
            lines.append((coords[0], Vector2D(coords[0].x + 1, coords[0].y)))
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

        # Preenche o fundo
        context.set_source_rgb(self._bg_color[0], self._bg_color[1], self._bg_color[2])
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        # Renderiza todos os objetos do display file
        for obj in self._display_file.objects:

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

    def on_button_press(self, w, event) -> None:
        '''
        Evento de clique.
        '''

        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            self._editor.handle_click(self.screen_to_world(Vector2D(event.x, event.y)))

    def on_button_release(self, w, event) -> None:
        '''
        Evento de liberação do mouse.
        '''

        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1:
            self._editor.handle_click(self.screen_to_world(Vector2D(event.x, event.y)))

    def on_size_allocate(self, allocation, user_data):
        '''
        Evento de alocação.
        '''

        self._window.bottom_right = Vector2D(user_data.width, user_data.height)
