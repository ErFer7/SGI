# -*- coding: utf-8 -*-

'''
Módulo para handlers de botões.
'''

import string
import gi

from source.viewport import ViewportHandler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ButtonHandler():

    button: Gtk.Widget
    button_id: string
    viewport: ViewportHandler

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
            # TO DO: escolher e criar um botão para definir cor, arrumar o signal aqui
            self.button.connect("???", self.on_color_button_value_changed)
        else:
            print("Erro: handler não encontrado: " + self.button_id)

    # Handlers ----------------------------------------------------------------
    def on_pen_button_clicked(self, obj):
        # TO DO: funcionamento alternativo para a função draw em viewport.py
        pass
    
    def on_line_button_clicked(self, obj):
        # TO DO: associar ao funcionamento atual da função draw
        pass

    def on_width_button_value_changed(self, obj):
        '''
        Botão de controle da largura dos traços.
        '''
        
        if self.button.get_name() == "GtkSpinButton":
            self.viewport.set_brush_width(self.button.get_value())

    def on_color_button_value_changed(self, obj):
        # TO DO: criar um botão para seleção de cor rgb
        #        (no Glade, nem vi qual componente usar e qual signal)

        # self.viewport.set_brush_color( -- INPUT -- )
        pass
