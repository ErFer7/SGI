'''
Módulo para o handler de configurações.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from gi.repository import Gtk

from source.handlers.handler import Handler

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow


class SettingsHandler(Handler):

    '''
    Handler de configurações.
    '''

    _clipping_method_button: Gtk.ToggleButton

    def __init__(self, handler_mediator: HandlerMediator, main_window: MainWindow) -> None:
        super().__init__(handler_mediator)

        settings_box = main_window.settings_box

        self._clipping_method_button = self.search_child_by_name(settings_box, 'Clipping method button')

        self._clipping_method_button.connect('toggled', self.toggle_clipping_method)

    def toggle_clipping_method(self, _) -> None:
        '''
        Muda o método de clipping.
        '''

        self.handler_mediator.manager_mediator.viewport_manager.change_clipping_method()

        if self._clipping_method_button.get_label() == 'Liang-Barsky':
            self._clipping_method_button.set_label('Cohen-Sutherland')
        else:
            self._clipping_method_button.set_label('Liang-Barsky')
