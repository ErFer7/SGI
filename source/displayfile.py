# -*- coding: utf-8 -*-

'''
Módulo para o handler do display file.
'''

import gi

from source.wireframe import Object

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

    def __init__(self, display_file_list: Gtk.ListStore) -> None:

        self.objects = []
        self._display_file_list = display_file_list

    # Métodos utilitários
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

    def remove_all(self) -> None:
        '''
        Remove todos os objetos.
        '''

        self.objects.clear()
        self._display_file_list.clear()
