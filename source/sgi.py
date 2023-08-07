# -*- coding: utf-8 -*-

'''
Classe principal do SGI.
'''

import gi

gi.require_version("Gtk", "3.0")

# pylint: disable=wrong-import-position
from gi.repository import Gtk # type: ignore

from source.handlers.main_window import MainWindow
from source.handlers.handler_mediator import HandlerMediator
from source.managers.object_manager import ObjectManager
from source.managers.manager_mediator import ManagerMediator
from source.handlers.main_window_handler import MainWindowHandler
from source.handlers.object_list_handler import ObjectListHandler
from source.handlers.creator_handler import CreatorHandler
from source.handlers.object_transform_handler import ObjectTransformHandler
from source.handlers.transformations_handler import TransformationsHandler
from source.handlers.settings_handler import SettingsHandler
from source.handlers.viewport_handler import ViewportHandler
from source.managers.viewport_manager import ViewportManager


class SGI():

    '''
    Sistema Gráfico Interativo (SGI).
    '''

    _main_window: MainWindow

    _handler_mediator: HandlerMediator
    _manager_mediator: ManagerMediator

    _main_window_handler: MainWindowHandler
    _object_list_handler: ObjectListHandler
    _creator_handler: CreatorHandler
    _object_transform_handler: ObjectTransformHandler
    _transformations_handler: TransformationsHandler
    _settings_handler: SettingsHandler
    _viewport_handler: ViewportHandler

    _object_list_manager: ObjectManager
    _viewport_manager: ViewportManager

    def __init__(self):
        self._main_window = MainWindow()

        self._handler_mediator = HandlerMediator()
        self._manager_mediator = ManagerMediator()

        self._handler_mediator.manager_mediator = self._manager_mediator
        self._manager_mediator.handler_mediator = self._handler_mediator

        self._main_window_handler = MainWindowHandler(self._handler_mediator, self._main_window)
        self._object_list_handler = ObjectListHandler(self._handler_mediator, self._main_window)
        self._creator_handler = CreatorHandler(self._handler_mediator, self._main_window)
        self._object_transform_handler = ObjectTransformHandler(self._handler_mediator, self._main_window)
        self._transformations_handler = TransformationsHandler(self._handler_mediator, self._main_window)
        self._settings_handler = SettingsHandler(self._handler_mediator, self._main_window)
        self._viewport_handler = ViewportHandler(self._handler_mediator, self._main_window)

        self._handler_mediator.set_handlers(self._main_window_handler,
                                            self._object_list_handler,
                                            self._creator_handler,
                                            self._object_transform_handler,
                                            self._transformations_handler,
                                            self._settings_handler,
                                            self._viewport_handler)

        self._object_list_manager = ObjectManager(self._manager_mediator)
        self._viewport_manager = ViewportManager(self._manager_mediator)

        self._manager_mediator.set_managers(self._object_list_manager, self._viewport_manager)

    def run(self) -> None:
        '''
        Executa a aplicação.
        '''

        self._main_window.show()
        Gtk.main()
