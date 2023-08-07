# -*- coding: utf-8 -*-

'''
Módulo para a interface de usuário.
'''

import os
import gi

gi.require_version('Gtk', '3.0')

# pylint: disable=wrong-import-position
from gi.repository import Gtk # type: ignore

from source.internals.transform import Vector
from source.managers.viewport_manager import ViewportManager


@Gtk.Template(filename=os.path.join(os.getcwd(), 'templates', 'template.ui'))
class MainWindow(Gtk.Window):

    '''
    Janela principal.
    '''

    __gtype_name__ = 'MainWindow'

    object_list_box: Gtk.Box = Gtk.Template.Child()
    display_file_list: Gtk.ListStore = Gtk.Template.Child()
    creator_box: Gtk.Box = Gtk.Template.Child()
    object_transform_box: Gtk.Box = Gtk.Template.Child()
    transformations_box: Gtk.Box = Gtk.Template.Child()
    settings_box: Gtk.Box = Gtk.Template.Child()
    viewport_drawing_area: Gtk.DrawingArea = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()

        self.maximize()

        self.viewport_handler = ViewportManager(self, Vector(25.0, 25.0, 0.0))
