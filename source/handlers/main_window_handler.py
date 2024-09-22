'''
Módulo do handler da janela principal.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from gi.repository import Gtk

from source.handlers.handler import Handler

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow


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

    def on_key_press(self, _, event) -> None:
        '''
        Evento de pressionamento de tecla
        '''

        self.handler_mediator.viewport_handler.handle_key_press(event.string)
