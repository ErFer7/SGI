# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from source.displayfile import DisplayFileHandler
from turtle import width
import string
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class ViewportHandler():

    '''
    Definição do viewport, este viewport é um handler para um widget DrawingArea.
    '''

    drawing_area: Gtk.DrawingArea
    display_file: DisplayFileHandler
    coords: list = [] # coordenadas de um novo objeto, dadas por cliques na drawing_area

    brush_width: float = 1.0
    brush_color: list = [1, 1, 1] # RGB
    drawing_mode: string = "line" # sem uso ainda

    def __init__(self, drawing_area: Gtk.DrawingArea, display_file: DisplayFileHandler) -> None:     
        self.drawing_area = drawing_area
        self.drawing_area.connect("draw", self.on_draw)
        self.drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.drawing_area.connect("button-press-event", self.on_button_press)
        self.display_file = display_file
        
    def set_brush_width(self, width_val: float):
        self.brush_width = width_val

    def set_brush_color(self, color_rgb: list):
        self.brush_color = color_rgb

    def draw_object(self, object: list, context):
        '''
        Renderização de objetos.
        '''

        # object: list = [type, pos[x,y], width, color[r,g,b]]
        type = object[0]
        pos = object[1]
        width = object[2]
        color = object[3]

        context.set_source_rgb(color[0], color[1], color[2])
        context.set_line_width(width)

        if type == "line": # duas coordenadas, i.e., pos.size() = 2
            context.move_to(pos[0][0], pos[0][1])
            context.line_to(pos[1][0], pos[1][1])
            context.stroke()
        # elif type == "wireframe": ...

    # Handlers ----------------------------------------------------------------
    def on_draw(self, area, context) -> None:
        '''
        Método para a renderização.
        '''

        # Preenche o fundo
        context.set_source_rgb(0, 0, 0)
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        # Define cor e largura do pincel
        context.set_source_rgb(self.brush_color[0], self.brush_color[1], self.brush_color[2])
        context.set_line_width(self.brush_width)

        # Adiciona objetos ao display file
        # --- o tipo (line) tá hardcoded pq ainda não temos wireframe etc
        if len(self.coords) > 1:
            new_object = ["line", self.coords, self.brush_width, self.brush_color]
            self.display_file.add_object(new_object)
            self.coords = []

        # Renderiza todos os objetos do display file
        for object in self.display_file.get_display_file():
            self.draw_object(object, context)

    def on_button_press(self, w, e):
        '''
        Evento de clique.
        '''

        if e.type == Gdk.EventType.BUTTON_PRESS and e.button == 1:
            self.coords.append([e.x, e.y])
            self.drawing_area.queue_draw()
