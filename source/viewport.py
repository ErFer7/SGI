# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from source.editor import EditorHandler
from source.wireframe import Line, Point, Rectangle
from source.displayfile import DisplayFileHandler

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class ViewportHandler():

    '''
    Definição do viewport, este viewport é um handler para um widget DrawingArea.
    '''

    # Atributos privados
    _brush_color: tuple
    _brush_width: float
    _window: Rectangle
    _bg_color: tuple
    _drawing_area: Gtk.DrawingArea
    _display_file: DisplayFileHandler
    _editor: EditorHandler

    def __init__(self,
                 drawing_area: Gtk.DrawingArea,
                 display_file: DisplayFileHandler,
                 editor: EditorHandler,
                 bg_color: tuple = (0, 0, 0)) -> None:

        self._drawing_area = drawing_area
        self._drawing_area.connect("draw", self.on_draw)
        self._drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self._drawing_area.connect("button-press-event", self.on_button_press)
        self._display_file = display_file
        self._editor = editor
        self._bg_color = bg_color
        self._coord = []
        self._brush_width = 1.0
        self._brush_color = (1, 1, 1)
        self._window = Rectangle((0.0, 0.0), (100.0, 100.0), "Window")  # Coordenadas no espaço vetorial do mundo

    # Métodos utilitários
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

            lines = self.coords_to_lines(obj.coord_list)
            color = obj.color
            line_width = obj.line_width

            # Define cor e largura do pincel
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)

            for line in lines:
                context.move_to(line[0][0], line[0][1])
                context.line_to(line[1][0], line[1][1])
                context.stroke()

    def on_button_press(self, w, e):
        '''
        Evento de clique.
        '''

        if e.type == Gdk.EventType.BUTTON_PRESS and e.button == 1:

            self._editor.handle_click((e.x, e.y))
            self._drawing_area.queue_draw()
