# -*- coding: utf-8 -*-

'''
Módulo do handler da janela principal.
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


class MainWindowHandler(Handler):

    '''
    Handler da janela principal.
    '''

    _user_call: bool

    def __init__(self, handler_mediator: HandlerMediator, main_window: MainWindow) -> None:
        super().__init__(handler_mediator)

        self._user_call = True

        main_window.connect('key-press-event', self.on_key_press)
        main_window.connect('destroy', Gtk.main_quit)

    @property
    def user_call(self) -> bool:
        '''
        Retorna se a chamada foi do usuário.
        '''

        return self._user_call

    @user_call.setter
    def user_call(self, value: bool) -> None:
        '''
        Define se a chamada foi do usuário.
        '''

        self._user_call = value

    # pylint: disable=unused-argument
    def on_key_press(self, widget, event) -> None:
        '''
        Evento de pressionamento de tecla
        '''

        self.handler_mediator.viewport_handler.handle_key_press(event.string)  # type: ignore
