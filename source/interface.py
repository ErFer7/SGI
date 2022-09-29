# -*- coding: utf-8 -*-

'''
Módulo para a interface de usuário.
'''

import os
import gi
from source.button import ButtonHandler
from source.displayfile import DisplayFileHandler
from source.editor import EditorHandler
from source.viewport import ViewportHandler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename=os.path.join(os.getcwd(), "interface", "interface_style.ui"))
class MainWindow(Gtk.Window):

    '''
    Janela principal.
    '''

    __gtype_name__ = "MainWindow"  # Nome da janela principal

    # Atributos privados
    viewport_handler: ViewportHandler
    display_file_handler: DisplayFileHandler
    editor_handler: EditorHandler

    # A ser visto
    pen_button_handler: ButtonHandler
    width_button_handler: ButtonHandler
    color_button_handler: ButtonHandler

    # Os trilhões de widgets vão aqui :p
    # Widgets
    viewport_drawing_area: Gtk.DrawingArea = Gtk.Template.Child()
    file_button: Gtk.MenuItem = Gtk.Template.Child()
    point_button: Gtk.Button = Gtk.Template.Child()
    line_button: Gtk.Button = Gtk.Template.Child()
    triangle_button: Gtk.Button = Gtk.Template.Child()
    rectangle_button: Gtk.Button = Gtk.Template.Child()
    polygon_button: Gtk.Button = Gtk.Template.Child()
    clear_button: Gtk.Button = Gtk.Template.Child()
    mode_label: Gtk.Label = Gtk.Template.Child()
    width_button: Gtk.SpinButton = Gtk.Template.Child()
    color_button: Gtk.ColorButton = Gtk.Template.Child()

    def __init__(self) -> None:

        super().__init__()

        self.display_file_handler = DisplayFileHandler()
        self.editor_handler = EditorHandler(self.display_file_handler,
                                            self.file_button,
                                            self.point_button,
                                            self.line_button,
                                            self.triangle_button,
                                            self.rectangle_button,
                                            self.polygon_button,
                                            self.clear_button,
                                            self.width_button,
                                            self.color_button,
                                            self.mode_label)
        self.viewport_handler = ViewportHandler(self.viewport_drawing_area,
                                                self.display_file_handler,
                                                self.editor_handler)

        self.connect("destroy", Gtk.main_quit)
