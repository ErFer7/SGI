# -*- coding: utf-8 -*-

'''
Módulo do handler da lista de objetos.
'''

from os.path import join

import gi

gi.require_version('Gtk', '3.0')

# pylint: disable=wrong-import-position
from gi.repository import Gtk # type: ignore

from source.handlers.handler_utils import HandlerUtils
from source.managers.object_manager import ObjectManager
from source.internals.wireframe import Object


class ObjectListHandler():

    '''
    Handler da lista de objetos.
    '''

    _display_file_list: Gtk.ListStore
    _file_name_entry: Gtk.Entry
    _load_button: Gtk.Entry
    _save_button: Gtk.Entry
    _object_list_manager: ObjectManager

    def __init__(self,
                 object_list_box: Gtk.Box,
                 display_file_list: Gtk.ListStore,
                 object_list_manager: ObjectManager) -> None:
        self._display_file_list = display_file_list
        self._object_list_manager = object_list_manager
        self._file_name_entry = HandlerUtils.search_child_by_name(object_list_box, 'File name entry')
        self._load_button = HandlerUtils.search_child_by_name(object_list_box, 'Load button')
        self._save_button = HandlerUtils.search_child_by_name(object_list_box, 'Save button')

        self._object_list_manager.set_object_list_handler(self)

        self._load_button.connect("clicked", self.load_file)
        self._save_button.connect("clicked", self.save_file)

    # pylint: disable=unused-argument
    def load_file(self, user_data) -> None:
        '''
        Carrega um arquivo.
        '''

        file_name = self._file_name_entry.get_text()
        self._object_list_manager.load_file(join("objects", file_name))
        self._rotation_anchor = self._focus_object.position
        self.update_spin_buttons()

    # pylint: disable=unused-argument
    def save_file(self, user_data) -> None:
        '''
        Salva um arquivo.
        '''

        file_name = self._file_name_entry.get_text()
        self._object_list_manager.save_file(join("objects", file_name))

    def add_object_register(self, obj: Object) -> None:
        '''
        Adiciona um registro na lista de objetos da interface.
        '''

        self._display_file_list.append([obj.name, str(obj.position)])

    def remove_object_register(self, index: int) -> None:
        '''
        Remove um registro da lista de objetos da interface.
        '''

        self._display_file_list.remove(self._display_file_list[index].iter)

    def update_object_info(self, index: int, info: str) -> None:
        '''
        Atualiza as informações de um objeto.
        '''

        self._display_file_list[index][1] = info
