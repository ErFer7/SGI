# -*- coding: utf-8 -*-

'''
Módulo para o handler do display file.
'''

import gi

from source.wireframe import Object
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
        self._display_file_list = display_file_list

    # Métodos
    def add_object(self, obj: Object) -> None:
        '''
        Adiciona um objeto.
        '''

        self.objects.append(obj)
        self._display_file_list.append([obj.name, str(obj.position)])

    # Por enquanto o id é o nome
    def remove_object(self, identification: str) -> None:
        '''
        Remove um objeto.
        '''

        for obj in self.objects:

            if obj.identification == identification:
                self.objects.remove(obj)
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

    def save_world(self) -> None:
        '''
        ...
        '''

        # file_system.afafjka

    def normalize_objects(self, window_center: Vector) -> None:
        '''
        '''
