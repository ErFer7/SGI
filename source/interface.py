# -*- coding: utf-8 -*-

'''
Módulo para a interface de usuário.
'''

import os
import gi
from source.button import ButtonHandler
from source.displayfile import DisplayFileHandler
from source.viewport import ViewportHandler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename=os.path.join(os.getcwd(), "interface", "interface_style.ui"))
class MainWindow(Gtk.Window):

    '''
    Janela principal.
    '''

    __gtype_name__ = "MainWindow"  # Nome da janela principal

    # Atributos ---------------------------------------------------------------
    viewport_handler: ViewportHandler
    pen_button_handler: ButtonHandler
    width_button_handler: ButtonHandler
    line_button_handler: ButtonHandler
    # displayfile_handler: DisplayFileHandler

    # Obtém os widgets a serem conectados com seus handlers
    viewport_drawing_area: Gtk.DrawingArea = Gtk.Template.Child()
    pen_button: Gtk.Button = Gtk.Template.Child()
    width_button: Gtk.SpinButton = Gtk.Template.Child()
    line_button: Gtk.Button = Gtk.Template.Child()

    # Construtor --------------------------------------------------------------
    def __init__(self) -> None:

        super().__init__()

        self.viewport_handler = ViewportHandler(self.viewport_drawing_area)
        self.pen_button_handler = ButtonHandler(self.pen_button, "pen_button")
        self.width_button_handler = ButtonHandler(self.width_button, "width_button")
        self.line_button_handler = ButtonHandler(self.line_button, "line_button")
        self.connect("destroy", Gtk.main_quit)
