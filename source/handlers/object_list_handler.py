# -*- coding: utf-8 -*-

'''
Módulo do handler da lista de objetos.
'''


from __future__ import annotations
from typing import TYPE_CHECKING

from os.path import join

import gi

gi.require_version('Gtk', '3.0')

# pylint: disable=wrong-import-position
from gi.repository import Gtk # type: ignore

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow

from source.internals.wireframe import Object
from source.handlers.handler import Handler


class ObjectListHandler(Handler):

    '''
    Handler da lista de objetos.
    '''

    _display_file_list: Gtk.ListStore
    _file_name_entry: Gtk.Entry
    _load_button: Gtk.Entry
    _save_button: Gtk.Entry

    def __init__(self, handler_mediator: HandlerMediator, main_window: MainWindow) -> None:
        super().__init__(handler_mediator)

        self._display_file_list = main_window.display_file_list

        object_list_box = main_window.object_list_box

        self._file_name_entry = self.search_child_by_name(object_list_box, 'File name entry')
        self._load_button = self.search_child_by_name(object_list_box, 'Load button')
        self._save_button = self.search_child_by_name(object_list_box, 'Save button')

        self._load_button.connect('clicked', self.load_file)
        self._save_button.connect('clicked', self.save_file)

    # pylint: disable=unused-argument
    def load_file(self, user_data) -> None:
        '''
        Carrega um arquivo.
        '''

        file_name = self._file_name_entry.get_text()
        anchor = self._handler_mediator.manager_mediator.object_manager.object_in_focus.position  # type: ignore
        object_manager = self._handler_mediator.manager_mediator.object_manager  # type: ignore

        object_manager.load_file(join('assets', 'objects', file_name))  # type: ignore
        self._handler_mediator.transformations_handler.update_object_rotation_anchor(anchor)  # type: ignore
        self._handler_mediator.object_transform_handler.update_spin_buttons()  # type: ignore
        self._handler_mediator.transformations_handler.update_rotation_anchor_spin_buttons()  # type: ignore

    # pylint: disable=unused-argument
    def save_file(self, user_data) -> None:
        '''
        Salva um arquivo.
        '''

        file_name = self._file_name_entry.get_text()

        object_manager = self._handler_mediator.manager_mediator.object_manager  # type: ignore
        object_manager.save_file(join('assets', 'objects', file_name))  # type: ignore

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
