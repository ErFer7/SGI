# -*- coding: utf-8 -*- 

'''
Módulo para o handler de configurações.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

import gi

gi.require_version('Gtk', '3.0')

# pylint: disable=wrong-import-position
from gi.repository import Gtk # type: ignore

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow

from source.handlers.handler import Handler


class SettingsHandler(Handler):

    '''
    Handler de configurações.
    '''

    _clipping_method_button: Gtk.ToggleButton

    def __init__(self, handler_mediator: HandlerMediator, main_window: MainWindow) -> None:
        super().__init__(handler_mediator)

        settings_box = main_window.settings_box

        self._clipping_method_button = self.search_child_by_name(settings_box, 'Clipping method button')

        self._clipping_method_button.connect("toggled", self.toggle_clipping_method)

    def toggle_clipping_method(self, user_data) -> None:
        '''
        Muda o método de clipping.
        '''

        self._main_window.viewport_handler.change_clipping_method()

        if self._clipping_method_button.get_label() == "Liang-Barsky":
            self._clipping_method_button.set_label("Cohen-Sutherland")
        else:
            self._clipping_method_button.set_label("Liang-Barsky")
