'''
Classe principal do SGI.
'''

from gi.repository import Gtk

from source.backend.backend import Backend
from source.frontend.viewport_handler import ViewportHandler
from source.frontend.settings_handler import SettingsHandler
from source.frontend.transformations_handler import TransformationsHandler
from source.frontend.object_transform_handler import ObjectTransformHandler
from source.frontend.creator_handler import CreatorHandler
from source.frontend.object_list_handler import ObjectListHandler
from source.frontend.main_window_handler import MainWindowHandler
from source.frontend.handler_mediator import HandlerMediator
from source.frontend.main_window import MainWindow


class SGI():

    '''
    Sistema Gráfico Interativo (SGI).
    '''

    _main_window: MainWindow

    _handler_mediator: HandlerMediator

    _main_window_handler: MainWindowHandler
    _object_list_handler: ObjectListHandler
    _creator_handler: CreatorHandler
    _object_transform_handler: ObjectTransformHandler
    _transformations_handler: TransformationsHandler
    _settings_handler: SettingsHandler
    _viewport_handler: ViewportHandler

    _backend: Backend

    def __init__(self):
        self._main_window = MainWindow()

        self._backend = Backend()

        self._handler_mediator = HandlerMediator()

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

    def run(self) -> None:
        '''
        Executa a aplicação.
        '''

        self._main_window.show()
        Gtk.main()
