# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from random import randrange
from source.displayfile import DisplayFileHandler
import string
import gi

from source.wireframe import Line, Object

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class ViewportHandler():

    '''
    Definição do viewport, este viewport é um handler para um widget DrawingArea.
    '''

    drawing_area: Gtk.DrawingArea
    display_file: DisplayFileHandler
    bg_color: tuple
    coords: list # coordenadas de um novo objeto, dadas por cliques na drawing_area
    coord_cache: list # Temporário
    brush_width: float
    brush_color: tuple

    # Acredito que não terá uso
    drawing_mode: string = "line" # sem uso ainda

    def __init__(self,
                 drawing_area: Gtk.DrawingArea,
                 display_file: DisplayFileHandler,
                 bg_color: tuple = (0, 0, 0)) -> None:

        self.drawing_area = drawing_area
        self.drawing_area.connect("draw", self.on_draw)
        self.drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.drawing_area.connect("button-press-event", self.on_button_press)
        self.display_file = display_file
        self.bg_color = bg_color
        self.coords = []
        self.coord_cache = []
        self.brush_width = 1.0
        self.brush_color = (1, 1, 1)
        
    def set_brush_width(self, width_val: float):
        self.brush_width = width_val

    def set_brush_color(self, color_rgb: tuple):
        self.brush_color = color_rgb

    # Handlers ----------------------------------------------------------------
    def on_draw(self, area, context) -> None:
        '''
        Método para a renderização.
        '''

        # Preenche o fundo
        context.set_source_rgb(self.bg_color[0], self.bg_color[1], self.bg_color[2])
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        # Renderiza todos os objetos do display file
        for obj in self.display_file.objects:

            self.coords = obj.get_coord_list()
            color = obj.color
            line_width = obj.line_width

            # Define cor e largura do pincel
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)

            for i, _ in enumerate(self.coords):

                if i < len(self.coords) - 1:
                    context.move_to(self.coords[i][0], self.coords[i][1])
                    context.line_to(self.coords[i + 1][0], self.coords[i + 1][1])
                    context.stroke()

            # Adiciona objetos ao display file
            # --- o tipo (line) tá hardcoded pq ainda não temos wireframe etc
            # if len(self.coords) > 1:
            #     new_object = ["line", self.coords, self.brush_width, self.brush_color]
            #     self.display_file.add_object(new_object)
            #     self.coords = []


    def on_button_press(self, w, e):
        '''
        Evento de clique.
        '''

        if e.type == Gdk.EventType.BUTTON_PRESS and e.button == 1:

            self.coord_cache.append([e.x, e.y])

            # if drawing_mode == "line":
            if len(self.coord_cache) > 1:

                self.display_file.add_object(Line(self.coord_cache[0][0],
                                                  self.coord_cache[0][1],
                                                  self.coord_cache[1][0],
                                                  self.coord_cache[1][1],
                                                  '',
                                                  self.brush_color,
                                                  self.brush_width))
                
                self.coord_cache.clear()
                self.drawing_area.queue_draw()
