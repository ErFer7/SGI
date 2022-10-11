# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from source.editor import EditorHandler
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
        self._drawing_area.connect("size-allocate", self.on_size_allocate)
        self._display_file = display_file
        self._editor = editor
        self._bg_color = bg_color
        self._window = Rectangle((0.0, 0.0),
                                 (922.0, 623.0),
                                 "Window",
                                 (0.5, 0.0, 0.5),
                                 2.0)  # Coordenadas no espaço vetorial do mundo

    # Métodos utilitários
    def world_to_screen(self, coord: tuple) -> tuple:
        '''
        Converte a coordenada de mundo para uma coordenada de tela.
        '''

        top_left = self._window.top_left
        bottom_right = self._window.bottom_right

        x_vp = ((coord[0] - top_left[0]) / (bottom_right[0] - top_left[0])) \
               * self._drawing_area.get_allocated_width()
        y_vp = (1 - (coord[1] - top_left[1]) / (bottom_right[1] - top_left[1])) \
               * self._drawing_area.get_allocated_height()

        return (x_vp, y_vp)

    def screen_to_world(self, coord: tuple) -> tuple:
        '''
        Converte a coordenada de tela para uma coordenada de mundo.
        '''

        return (coord[0], self._window.bottom_right[1] - coord[1])

    def coords_to_lines(self, coords: list) -> list:
        '''
        Converte coordenadas normais para linhas.
        '''

        lines = []

        if len(coords) == 1:
            lines.append((coords[0], (coords[0][0] + 1, coords[0][1])))
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

            # print(screen_coords)

            lines = self.coords_to_lines(screen_coords)
            color = obj.color
            line_width = obj.line_width

            # Define cor e largura do pincel
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)

            for line in lines:
                context.move_to(line[0][0], line[0][1])
                context.line_to(line[1][0], line[1][1])
                context.stroke()

        lines = self.coords_to_lines(self._window.coord_list)
        color = self._window.color
        line_width = self._window.line_width

        # Define cor e largura do pincel
        context.set_source_rgb(color[0], color[1], color[2])
        context.set_line_width(line_width)

        for line in lines:
            context.move_to(line[0][0], line[0][1])
            context.line_to(line[1][0], line[1][1])
            context.stroke()

        self._drawing_area.queue_draw()

    def on_button_press(self, w, event) -> None:
        '''
        Evento de clique.
        '''

        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            self._editor.handle_click(self.screen_to_world((event.x, event.y)))

    def on_size_allocate(self, allocation, user_data):
        '''
        Evento de alocação.
        '''

        self._window.bottom_right = (user_data.width, user_data.height)
