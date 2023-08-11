# -*- coding: utf-8 -*-

'''
Módulo para o mediador de gerenciadores.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from source.managers.object_manager import ObjectManager
from source.managers.viewport_manager import ViewportManager

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator


class ManagerMediator():

    '''
    Mediador de gerenciadores.
    '''

    _handler_mediator: HandlerMediator | None
    _object_manager: ObjectManager | None
    _viewport_manager: ViewportManager | None

    def __init__(self) -> None:
        self._handler_mediator = None
        self._object_manager = None
        self._viewport_manager = None

    @property
    def handler_mediator(self) -> HandlerMediator | None:
        '''
        Retorna o mediador de handlers.
        '''

        return self._handler_mediator

    @property
    def object_manager(self) -> ObjectManager | None:
        '''
        Retorna o gerenciador de objetos.
        '''

        return self._object_manager

    @property
    def viewport_manager(self) -> ViewportManager | None:
        '''
        Retorna o gerenciador de viewport.
        '''

        return self._viewport_manager

    @handler_mediator.setter
    def handler_mediator(self, handler_mediator: HandlerMediator) -> None:
        '''
        Define o mediador de handlers.
        '''

        self._handler_mediator = handler_mediator

    def set_managers(self, **managers) -> None:
        '''
        Define os gerenciadores.
        '''

        self._object_manager = managers['object_manager']
        self._viewport_manager = managers['viewport_manager']
