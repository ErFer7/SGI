'''
Módulo para o handler do display file.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from source.backend.objects.object import Object
from source.backend.objects.wireframes_2d import Line
from source.backend.file_system import FileSystem
from source.backend.math.vector import Vector
from source.managers.manager import Manager

if TYPE_CHECKING:
    from source.managers.manager_mediator import ManagerMediator


class ObjectManager(Manager):

    '''
    Nesta classe os objetos seriam armazenados e transferidos para o viewport quando necessário.
    '''

    _default_objects: list[Object]
    _objects: list[Object]
    _file_system: FileSystem
    _object_in_focus: Object | None

    def __init__(self, manager_mediator: ManagerMediator) -> None:
        super().__init__(manager_mediator)

        self._default_objects = []
        self._objects = []
        self._file_system = FileSystem()
        self._object_in_focus = None

        self._default_objects.append(Line(Vector(100.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0), 'X Axis', (1.0, 0.25, 0.25)))
        self._default_objects.append(Line(Vector(0.0, 100.0, 0.0), Vector(0.0, 0.0, 0.0), 'Y Axis', (0.25, 1.0, 0.25)))
        self._default_objects.append(Line(Vector(0.0, 0.0, 100.0), Vector(0.0, 0.0, 0.0), 'Z Axis', (0.25, 0.25, 1.0)))

    @property
    def objects(self) -> list[Object]:
        '''
        Retorna a lista de objetos.
        '''

        return self._objects + self._default_objects

    @property
    def object_in_focus(self) -> Object | None:
        '''
        Retorna o objeto em foco.
        '''

        return self._object_in_focus

    @object_in_focus.setter
    def object_in_focus(self, obj: Object | None) -> None:
        '''
        Define o objeto em foco.
        '''

        self._object_in_focus = obj

    def get_last(self) -> Object:
        '''
        Retorna o último objeto da lista.
        '''

        return self._objects[-1]

    def set_last_as_focus(self) -> None:
        '''
        Define o último objeto da lista como foco.
        '''

        self._object_in_focus = self._objects[-1]

    def add_object(self, obj: Object) -> None:
        '''
        Adiciona um objeto.
        '''

        self._objects.append(obj)

        object_list_handler = self._manager_mediator.handler_mediator.object_list_handler
        object_list_handler.add_object_register(obj)

    def update_object_info(self, index: int) -> None:
        '''
        Atualiza as informações de um objeto.
        '''

        object_list_handler = self._manager_mediator.handler_mediator.object_list_handler
        object_list_handler.update_object_info(index, str(self._objects[index].position))

    def remove_last(self) -> None:
        '''
        Remove o último objeto.
        '''

        if len(self._objects) > 0:
            object_list_handler = self._manager_mediator.handler_mediator.object_list_handler

            self._objects.pop()
            object_list_handler.remove_object_register(-1)

    def load_file(self, file_name: str) -> None:
        '''
        Carrega um arquivo.
        '''

        loaded = self._file_system.load_scene(file_name)

        for obj in loaded:
            self.add_object(obj)

        self._object_in_focus = self._objects[-1]

    def save_file(self, file_name: str) -> None:
        '''
        Salva um arquivo.
        '''

        self._file_system.save_scene(file_name, self._objects)
