'''
Classe principal do SGI.
'''

from gi.repository import Gtk

from source.backend.math.transform import Vector
from source.managers.viewport_manager import ViewportManager
from source.handlers.viewport_handler import ViewportHandler
from source.handlers.settings_handler import SettingsHandler
from source.handlers.transformations_handler import TransformationsHandler
from source.handlers.object_transform_handler import ObjectTransformHandler
from source.handlers.creator_handler import CreatorHandler
from source.handlers.object_list_handler import ObjectListHandler
from source.handlers.main_window_handler import MainWindowHandler
from source.managers.manager_mediator import ManagerMediator
from source.managers.object_manager import ObjectManager
from source.handlers.handler_mediator import HandlerMediator
from source.handlers.main_window import MainWindow


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

    _object_manager: ObjectManager
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

        self._handler_mediator.set_handlers(main_window_handler=self._main_window_handler,
                                            object_list_handler=self._object_list_handler,
                                            creator_handler=self._creator_handler,
                                            object_transform_handler=self._object_transform_handler,
                                            transformations_handler=self._transformations_handler,
                                            settings_handler=self._settings_handler,
                                            viewport_handler=self._viewport_handler)

        self._object_manager = ObjectManager(self._manager_mediator)
        self._viewport_manager = ViewportManager(self._manager_mediator, Vector(25.0, 25.0, 0.0), (0.05, 0.05, 0.05))

        self._manager_mediator.set_managers(object_manager=self._object_manager,
                                            viewport_manager=self._viewport_manager)

    def run(self) -> None:
        '''
        Executa a aplicação.
        '''

        self._main_window.show()
        Gtk.main()
