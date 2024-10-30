'''
Backend do SGI.
'''


from uuid import uuid4
from source.backend.files.file_system import FileManager
from source.backend.math.vector import Vector
from source.backend.objects.object import Object
from source.backend.rendering.renderer import Renderer
from source.backend.objects.object_manager import ObjectManager


class Backend():

    '''
    Backend.
    '''

    _object_manager: ObjectManager
    _renderer: Renderer

    def __init__(self) -> None:
        self._object_manager = ObjectManager()
        self._renderer = Renderer()

    # Interface com o ObjectManager
    @property
    def objects(self) -> tuple[Object]:
        '''
        Retorna os objetos.
        '''

        return self._object_manager.objects

    @property
    def selected_object(self) -> Object | None:
        '''
        Retorna o objeto selecionado.
        '''

        return self._object_manager.selected_object

    def select_object(self, object_id: uuid4) -> None:
        '''
        Seleciona um objeto.
        '''

        self._object_manager.select_object(object_id)

    def deselect_object(self) -> None:
        '''
        Deseleciona um objeto.
        '''

        self._object_manager.deselect_object()

    def add_object(self, object_: Object) -> None:
        '''
        Adiciona um objeto.
        '''

        self._object_manager.add_object(object_)

    def remove_object(self, object_id: uuid4) -> None:
        '''
        Remove um objeto.
        '''

        self._object_manager.remove_object(object_id)

    def remove_selected_object(self) -> None:
        '''
        Remove o objeto selecionado.
        '''

        self._object_manager.remove_selected_object()

    def move_window(self, direction: Vector) -> None:
        '''
        Move a window.
        '''

        self._object_manager.window.translate(direction)

    def rotate_window(self, rotation: Vector) -> None:
        '''
        Rotaciona a window.
        '''

        self._object_manager.window.rotate(rotation)

    def reescale_window(self, scale: Vector) -> None:
        '''
        Reescala a window.
        '''

        self._object_manager.window.rescale(scale)

    def reset_window(self) -> None:
        '''
        Redefine a posição da window.
        '''

        self._object_manager.window.reset()

    def resize_window(self, extension: Vector) -> None:
        '''
        Redefine a extensão da window.
        '''

        self._object_manager.window.resize(extension)

    # Interface com o File Manager
    def load_file(self, file_name: str) -> None:
        '''
        Carrega um arquivo.
        '''

        loaded_objects = FileManager.load_scene(file_name)

        for object_ in loaded_objects:
            self.add_object(object_)

        self._object_manager.select_object(loaded_objects[0].id)

    # Interface com o renderizador
    def render(self, area, context, screen_width: int, screen_height: int) -> None:
        '''
        Renderiza a cena.
        '''

        self._renderer.render(area,
                              context,
                              screen_width,
                              screen_height,
                              self._object_manager.window,
                              self._object_manager.objects)
