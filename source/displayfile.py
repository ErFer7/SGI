# -*- coding: utf-8 -*-

'''
Módulo para o handler do display file.
'''

from math import degrees
from os.path import join

import gi

from source.wireframe import Object, Window
from source.file_system import FileSystem
from source.transform import Vector

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DisplayFileHandler():

    '''
    Nesta classe os objetos seriam armazenados e transferidos para o viewport quando necessário.
    '''

    # Atributos públicos
    objects: list[Object]

    # Atributos privados
    _display_file_list: Gtk.ListStore

    def __init__(self, display_file_list: Gtk.ListStore, file_system: FileSystem) -> None:

        self.objects = []
        self._all_objects_normalized = False
        self._display_file_list = display_file_list

        self.objects = file_system.load_scene(join("objects", "test.obj"))

    # Métodos
    def add_object(self, obj: Object) -> None:
        '''
        Adiciona um objeto.
        '''

        self.objects.append(obj)
        self._display_file_list.append([obj.name, str(obj.position)])
        self._all_objects_normalized = False

    # Por enquanto o id é o nome
    def remove_object(self, identification: str) -> None:
        '''
        Remove um objeto.
        '''

        for obj in self.objects:
            if obj.identification == identification:
                self.objects.remove(obj)
                self._all_objects_normalized = False
                break

    def update_object_info(self, index: int) -> None:
        '''
        Atualiza as informações de um objeto.
        '''

        self._display_file_list[index][1] = str(self.objects[index].position)

    def remove_last(self) -> None:
        '''
        Remove todos os objetos.
        '''

        if len(self.objects) > 0:
            self.objects.pop()
            self._display_file_list.remove(self._display_file_list[-1].iter)
            self._all_objects_normalized = False

    def save_world(self) -> None:
        '''
        Salva o mundo em um arquivo .obj.
        '''

        raise NotImplementedError

    def normalize_objects(self, window: Window) -> None:
        '''
        Normaliza todos os objetos.
        '''

        window_up = window.calculate_y_projected_vector()
        rotation = degrees(window_up * Vector(0.0, 1.0, 0.0))

        if window_up.x > 0.0:
            rotation = 360 - rotation

        for obj in self.objects + [window]:
            obj.normalize(window.position, window.scale, rotation)
