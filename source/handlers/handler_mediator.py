'''
Módulo do mediador de handlers.
'''

from source.handlers.creator_handler import CreatorHandler
from source.handlers.main_window_handler import MainWindowHandler
from source.handlers.object_list_handler import ObjectListHandler
from source.handlers.object_transform_handler import ObjectTransformHandler
from source.handlers.settings_handler import SettingsHandler
from source.handlers.transformations_handler import TransformationsHandler
from source.handlers.viewport_handler import ViewportHandler
from source.managers.manager_mediator import ManagerMediator


class HandlerMediator():

    '''
    Mediador.
    '''

    _manager_mediator: ManagerMediator | None
    _main_window_handler: MainWindowHandler | None
    _object_list_handler: ObjectListHandler | None
    _creator_handler: CreatorHandler | None
    _object_transform_handler: ObjectTransformHandler | None
    _transformations_handler: TransformationsHandler | None
    _settings_handler: SettingsHandler | None
    _viewport_handler: ViewportHandler | None

    def __init__(self) -> None:
        self._manager_mediator = None
        self._main_window_handler = None
        self._object_list_handler = None
        self._creator_handler = None
        self._object_transform_handler = None
        self._transformations_handler = None
        self._settings_handler = None
        self._viewport_handler = None

    @property
    def manager_mediator(self) -> ManagerMediator | None:
        '''
        Retorna o mediador de gerenciadores.
        '''

        return self._manager_mediator

    @property
    def main_window_handler(self) -> MainWindowHandler | None:
        '''
        Retorna o handler da janela principal.
        '''

        return self._main_window_handler

    @property
    def object_list_handler(self) -> ObjectListHandler | None:
        '''
        Retorna o handler da lista de objetos.
        '''

        return self._object_list_handler

    @property
    def creator_handler(self) -> CreatorHandler | None:
        '''
        Retorna o handler do criador.
        '''

        return self._creator_handler

    @property
    def object_transform_handler(self) -> ObjectTransformHandler | None:
        '''
        Retorna o handler da transformação de objetos.
        '''

        return self._object_transform_handler

    @property
    def transformations_handler(self) -> TransformationsHandler | None:
        '''
        Retorna o handler das transformações.
        '''

        return self._transformations_handler

    @property
    def settings_handler(self) -> SettingsHandler | None:
        '''
        Retorna o handler das configurações.
        '''

        return self._settings_handler

    @property
    def viewport_handler(self) -> ViewportHandler | None:
        '''
        Retorna o handler da viewport.
        '''

        return self._viewport_handler

    @manager_mediator.setter
    def manager_mediator(self, manager_mediator: ManagerMediator) -> None:
        '''
        Define o mediador de gerenciadores.
        '''

        self._manager_mediator = manager_mediator

    def set_handlers(self, **handlers) -> None:
        '''
        Define os handlers.
        '''

        self._main_window_handler = handlers['main_window_handler']
        self._object_list_handler = handlers['object_list_handler']
        self._creator_handler = handlers['creator_handler']
        self._object_transform_handler = handlers['object_transform_handler']
        self._transformations_handler = handlers['transformations_handler']
        self._settings_handler = handlers['settings_handler']
        self._viewport_handler = handlers['viewport_handler']
