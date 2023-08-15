# -*- coding: utf-8 -*-

'''
Módulo para o handler.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from gi.repository import Gtk

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator


class Handler():

    '''
    Hanlder.
    '''

    _handler_mediator: HandlerMediator

    def __init__(self, mediator: HandlerMediator) -> None:
        self._handler_mediator = mediator

    @property
    def handler_mediator(self) -> HandlerMediator:
        '''
        Retorna o mediador.
        '''

        return self._handler_mediator

    def search_child_by_name(self, widget: Gtk.Widget, name: str) -> Gtk.Widget | None:
        '''
        Busca um widget pelo nome.
        '''

        if widget.get_name() == name:
            return widget

        if issubclass(type(widget), Gtk.Container):
            for child in widget.get_children():
                sub_widget = self.search_child_by_name(child, name)

                if sub_widget is not None:
                    return sub_widget

        return None
