# -*- coding: utf-8 -*-

'''
Módulo para o handler de botões.
'''

import string
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject


class ButtonHandler():

    button: Gtk.Widget
    button_id: string

    def __init__(self, button: Gtk.Widget, button_id):
        self.button = button
        self.button_id = button_id
        self.select_handler(button_id)
        
        #    SE ISSO FUNCIONASSE...
        # handler = "self." + button_id + "()"
        # self.button.connect("clicked", handler) << string não é callable

    def select_handler(self, id):
        if id == "width_button":
            self.button.connect("change_value", self.width_button)
        elif id == "pen_button":
            self.button.connect("clicked", self.pen_button)
        elif id == "line_button":
            self.button.connect("clicked", self.line_button)
        else:
            print("Erro: handler não encontrado: " + self.button_id)

    # Handlers ----------------------------------------------------------------

    def width_button(self, obj):
        # TO DO: ler o valor do botão (SpinButton::Entry get_value) e
        #        atualizar a grossura do "pincel" em viewport.py
        pass

    def pen_button(self, obj):
        # TO DO: funcionamento alternativo para a função draw em viewport.py
        print("alo alo")
    
    def line_button(self, obj):
        # TO DO: associar ao funcionamento atual da função draw
        pass
