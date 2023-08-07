# -*- coding: utf-8 -*-

'''
Módulo para o gerenciador.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.managers.manager_mediator import ManagerMediator


class Manager():

    '''
    Gerenciador.
    '''

    _manager_mediator: ManagerMediator

    def __init__(self, manager_mediator: ManagerMediator) -> None:
        self._manager_mediator = manager_mediator
