# -*- coding: utf-8 -*-

'''
Módulo para a interface de usuário.
'''

import os
import gi
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

    # Os trilhões de widgets vão aqui :p
    # Widgets
    viewport_drawing_area: Gtk.DrawingArea = Gtk.Template.Child()
    file_button: Gtk.MenuItem = Gtk.Template.Child()
    point_button: Gtk.ToggleButton = Gtk.Template.Child()
    line_button: Gtk.ToggleButton = Gtk.Template.Child()
    triangle_button: Gtk.ToggleButton = Gtk.Template.Child()
    rectangle_button: Gtk.ToggleButton = Gtk.Template.Child()
    polygon_button: Gtk.ToggleButton = Gtk.Template.Child()
    width_button: Gtk.SpinButton = Gtk.Template.Child()
    color_button: Gtk.ColorButton = Gtk.Template.Child()
    edges_button: Gtk.SpinButton = Gtk.Template.Child()
    display_file_list: Gtk.ListStore = Gtk.Template.Child()
    remove_button: Gtk.Button = Gtk.Template.Child()
    position_x_button: Gtk.SpinButton = Gtk.Template.Child()
    position_y_button: Gtk.SpinButton = Gtk.Template.Child()
    position_z_button: Gtk.SpinButton = Gtk.Template.Child()
    scale_x_button: Gtk.SpinButton = Gtk.Template.Child()
    scale_y_button: Gtk.SpinButton = Gtk.Template.Child()
    scale_z_button: Gtk.SpinButton = Gtk.Template.Child()
    rotation_x_button: Gtk.SpinButton = Gtk.Template.Child()
    rotation_y_button: Gtk.SpinButton = Gtk.Template.Child()
    rotation_z_button: Gtk.SpinButton = Gtk.Template.Child()
    translate_x_button: Gtk.SpinButton = Gtk.Template.Child()
    translate_y_button: Gtk.SpinButton = Gtk.Template.Child()
    translate_z_button: Gtk.SpinButton = Gtk.Template.Child()
    apply_translation_button: Gtk.Button = Gtk.Template.Child()
    rescale_x_button: Gtk.SpinButton = Gtk.Template.Child()
    rescale_y_button: Gtk.SpinButton = Gtk.Template.Child()
    rescale_z_button: Gtk.SpinButton = Gtk.Template.Child()
    apply_scaling_button: Gtk.Button = Gtk.Template.Child()
    rotation_button: Gtk.SpinButton = Gtk.Template.Child()
    apply_rotation_button: Gtk.Button = Gtk.Template.Child()
    rotation_anchor_button: Gtk.Button = Gtk.Template.Child()
    rotation_anchor_button_x: Gtk.SpinButton = Gtk.Template.Child()
    rotation_anchor_button_y: Gtk.SpinButton = Gtk.Template.Child()
    rotation_anchor_button_z: Gtk.SpinButton = Gtk.Template.Child()

    def __init__(self) -> None:

        super().__init__()

        self.maximize()

        self.display_file_handler = DisplayFileHandler(self.display_file_list)
        self.editor_handler = EditorHandler(self,
                                            self.file_button,
                                            self.point_button,
                                            self.line_button,
                                            self.triangle_button,
                                            self.rectangle_button,
                                            self.polygon_button,
                                            self.width_button,
                                            self.color_button,
                                            self.edges_button,
                                            self.remove_button,
                                            self.position_x_button,
                                            self.position_y_button,
                                            self.position_z_button,
                                            self.scale_x_button,
                                            self.scale_y_button,
                                            self.scale_z_button,
                                            self.rotation_x_button,
                                            self.rotation_y_button,
                                            self.rotation_z_button,
                                            self.translate_x_button,
                                            self.translate_y_button,
                                            self.translate_z_button,
                                            self.apply_translation_button,
                                            self.rescale_x_button,
                                            self.rescale_y_button,
                                            self.rescale_z_button,
                                            self.apply_scaling_button,
                                            self.rotation_button,
                                            self.apply_rotation_button,
                                            self.rotation_anchor_button,
                                            self.rotation_anchor_button_x,
                                            self.rotation_anchor_button_y,
                                            self.rotation_anchor_button_z)
        self.viewport_handler = ViewportHandler(self, self.viewport_drawing_area)

        self.connect("destroy", Gtk.main_quit)
