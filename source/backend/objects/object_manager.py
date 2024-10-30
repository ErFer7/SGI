'''
Módulo para o handler do display file.
'''

from uuid import uuid4
from source.backend.objects.object import Object
from source.backend.objects.window import Window
from source.backend.objects.wireframes_2d import Line
from source.backend.math.vector import Vector


class ObjectManager():

    '''
    Nesta classe os objetos seriam armazenados e transferidos para o viewport quando necessário.
    '''

    _default_objects: list[Object]
    _objects: list[Object]
    _selected_object: Object | None
    _window: Window

    def __init__(self) -> None:
        self._default_objects = []
        self._objects = []
        self._selected_object = None
        self._window = Window(Vector(-500.0, -500.0),
                              Vector(500.0, 500.0),
                              Vector(0.0, 0.0, -500.0),
                              (0.5, 0.0, 0.5),
                              2.0)

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
    def selected_object(self) -> Object | None:
        '''
        Retorna o objeto em foco.
        '''

        return self._selected_object

    @property
    def window(self) -> Window:
        '''
        Retorna a janela.
        '''

        return self._window

    def select_object(self, object_id: uuid4) -> None:
        '''
        Seleciona um objeto.
        '''

        for object_ in self._objects:
            if object_.id == object_id:
                self._selected_object = object_

    def deselect_object(self) -> None:
        '''
        Deseleciona um objeto.
        '''

        self._selected_object = None

    def add_object(self, object_: Object) -> None:
        '''
        Adiciona um objeto.
        '''

        self._objects.append(object_)

    def remove_object(self, object_id: uuid4) -> None:
        '''
        Remove um objeto.
        '''

        for i, object_ in enumerate(self._objects):
            if object_.id == object_id:
                self._objects.pop(i)
                break

    def remove_selected_object(self) -> None:
        '''
        Remove o objeto em foco.
        '''

        if self._selected_object is not None:
            self.remove_object(self._selected_object.id)
            self._selected_object = None
