# -*- coding: utf-8 -*-

'''
Módulo para handlers de botões.
'''

from logging import setLogRecordFactory
import gi

from source.viewport import ViewportHandler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class ButtonHandler():

    button: Gtk.Widget
    button_id: str
    viewport: ViewportHandler
    # brush_color: Gdk.RGBA

    def __init__(self, button: Gtk.Widget, button_id, viewport: ViewportHandler = None) -> None:
        self.button = button
        self.button_id = button_id
        self.select_handler(button_id)
        self.viewport = viewport # para botões que precisam acessar a viewport

    def select_handler(self, id):
        if id == "pen_button":
            self.button.connect("clicked", self.on_pen_button_clicked)
        elif id == "line_button":
            self.button.connect("clicked", self.on_line_button_clicked)
        elif id == "width_button":
            self.button.connect("value_changed", self.on_width_button_value_changed)
        elif id == "color_button":
            # TODO: escolher e criar um botão para definir cor, arrumar o signal aqui
            self.button.connect("color_set", self.on_color_button_color_set)
        else:
            print("Erro: handler não encontrado: " + self.button_id)

    # Handlers ----------------------------------------------------------------
    def on_pen_button_clicked(self, obj):
        # TODO: funcionamento alternativo para a função draw em viewport.py
        pass

    def on_line_button_clicked(self, obj):
        # TODO: associar ao funcionamento atual da função draw
        pass

    def on_width_button_value_changed(self, obj):
        '''
        Botão de controle da largura dos traços.
        '''
        
        if self.button.get_name() == "GtkSpinButton":
            self.viewport.set_brush_width(self.button.get_value())

    def on_color_button_color_set(self, obj):
        rgb_string = self.button.get_rgba().to_string().strip("rgb()") # "rgb(r,g,b)"" -> "r,g,b"
        rgb = [int(val) for val in rgb_string.split(",")] # "r,g,b" -> [r, g, b]
        self.viewport.set_brush_color(tuple(rgb))