# -*- coding: utf-8 -*-

'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from turtle import width
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class ViewportHandler():

    '''
    Definição do viewport, este viewport é um handler para um widget DrawingArea.
    '''

    coords: list
    drawing_area: Gtk.DrawingArea
    brush_width: float = 1.0
    width_button: Gtk.Widget
    
    def __init__(self, drawing_area: Gtk.DrawingArea, width_button: Gtk.Widget) -> None:     
        self.drawing_area = drawing_area
        self.drawing_area.connect("draw", self.on_draw)
        self.drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.drawing_area.connect("button-press-event", self.on_button_press)
        self.coords = []
        
        self.width_button = width_button
        self.width_button.connect("value_changed", self.on_width_button_value_changed)

    # Handlers ----------------------------------------------------------------
    def on_draw(self, area, context) -> None:
        '''
        Método para a renderização.
        '''

        # Preenche o fundo
        context.set_source_rgb(0, 0, 0)
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        # Define uma linha
        context.set_source_rgb(1, 1, 1)
        context.set_line_width(self.brush_width)

        if len(self.coords) > 1:

            for i, _ in enumerate(self.coords):

                if i + 1 < len(self.coords):

                    context.move_to(self.coords[i][0], self.coords[i][1])
                    context.line_to(self.coords[i + 1][0], self.coords[i + 1][1])
                    context.stroke()

    def on_button_press(self, w, e):
        '''
        Evento de clique.
        '''

        if e.type == Gdk.EventType.BUTTON_PRESS and e.button == 1:
            self.coords.append([e.x, e.y])
            self.drawing_area.queue_draw()

    # --- fiz isso aqui pq não sei como fazer isso funcionar com o handler em button.py
    def on_width_button_value_changed(self, obj):
        '''
        Botão de controle da largura dos traços.
        '''
        
        if self.width_button.get_name() == "GtkSpinButton":
            self.brush_width = self.width_button.get_value()