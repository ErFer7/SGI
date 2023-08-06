# -*- coding: utf-8 -*-

'''
Classe principal do SGI.
'''

import gi

gi.require_version("Gtk", "3.0")

# pylint: disable=wrong-import-position
from gi.repository import Gtk # type: ignore

from source.handlers.main_window_handler import MainWindowHandler
from source.managers.object_manager import ObjectManager


class SGI():

    '''
    Sistema Gráfico Interativo (SGI).
    '''

    _main_window_handler: MainWindowHandler
    _object_list_manager: ObjectManager

    def __init__(self):
        self.object_list_manager = ObjectManager()
        self.main_window_handler = MainWindowHandler(self.object_list_manager)

        self.main_window_handler.show()

    def run(self) -> None:
        '''
        Executa a aplicação.
        '''

        self.main_window_handler.show()
        Gtk.main()
