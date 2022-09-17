# -*- coding: utf-8 -*-

'''
Módulo para handlers de botões.
'''

import string
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ButtonHandler():

    button: Gtk.Widget 
    button_id: string

    def __init__(self, button: Gtk.Widget, button_id) -> None:
        self.button = button
        self.button_id = button_id
        self.select_handler(button_id)

    def select_handler(self, id):
        if id == "pen_button":
            self.button.connect("clicked", self.on_pen_button_clicked)
        elif id == "line_button":
            self.button.connect("clicked", self.on_line_button_clicked)
        else:
            print("Erro: handler não encontrado: " + self.button_id)

    # Handlers ----------------------------------------------------------------
    def on_pen_button_clicked(self, obj):
        # TO DO: funcionamento alternativo para a função draw em viewport.py
        print("alo alo")
    
    def on_line_button_clicked(self, obj):
        # TO DO: associar ao funcionamento atual da função draw
        pass
