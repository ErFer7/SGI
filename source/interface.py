# -*- coding: utf-8 -*-

'''
Módolo para a interface de usuário.
'''

import os
import gi

from source.viewport import Viewport

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename=os.path.join(os.getcwd(), "interface", "interface_style.ui"))
class MainWindow(Gtk.Window):

    '''
    Janela princial.
    '''

    __gtype_name__ = "MainWindow"  # Nome da janela princial

    # Atributos ---------------------------------------------------------------
    viewport: Viewport
    # Obtém o widget com o id "viewport_drawing_area"
    viewport_drawing_area: Gtk.DrawingArea = Gtk.Template.Child()

    # Construtor --------------------------------------------------------------
    def __init__(self) -> None:

        super().__init__()

        self.viewport = Viewport()

        self.connect("destroy", Gtk.main_quit)
        self.viewport_drawing_area.connect("draw", self.viewport.on_draw)
