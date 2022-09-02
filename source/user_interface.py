# -*- coding: utf-8 -*-

'''
Módolo para a interface de usuário.
'''

import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow():

    '''
    Janela princial.
    '''

    window: None

    def __init__(self) -> None:

        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(os.getcwd(), "interface", "interface_style.glade"))

        self.window = builder.get_object("main_window")

    def show(self) -> None:
        '''
        Exibe a janela.
        '''

        self.window.show_all()
