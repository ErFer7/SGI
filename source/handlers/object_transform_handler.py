# -*- coding: utf-8 -*-

'''
Módulo para o editor de transformado de objetos.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

import gi
from gi.repository import Gtk

from source.internals.transform import Vector
from source.handlers.handler import Handler

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow

gi.require_version('Gtk', '3.0')


class ObjectTransformHandler(Handler):

    '''
    Editor de transformada de objetos.
    '''

    _position_x_button: Gtk.SpinButton
    _position_y_button: Gtk.SpinButton
    _position_z_button: Gtk.SpinButton
    _scale_x_button: Gtk.SpinButton
    _scale_y_button: Gtk.SpinButton
    _scale_z_button: Gtk.SpinButton
    _rotation_x_button: Gtk.SpinButton
    _rotation_y_button: Gtk.SpinButton
    _rotation_z_button: Gtk.SpinButton

    def __init__(self, handler_mediator: HandlerMediator, main_window: MainWindow) -> None:
        super().__init__(handler_mediator)

        object_transform_box = main_window.object_transform_box

        self._position_x_button = self.search_child_by_name(object_transform_box, 'Position x button')
        self._position_y_button = self.search_child_by_name(object_transform_box, 'Position y button')
        self._position_z_button = self.search_child_by_name(object_transform_box, 'Position z button')
        self._scale_x_button = self.search_child_by_name(object_transform_box, 'Scale x button')
        self._scale_y_button = self.search_child_by_name(object_transform_box, 'Scale y button')
        self._scale_z_button = self.search_child_by_name(object_transform_box, 'Scale z button')
        self._rotation_x_button = self.search_child_by_name(object_transform_box, 'Rotation x button')
        self._rotation_y_button = self.search_child_by_name(object_transform_box, 'Rotation y button')
        self._rotation_z_button = self.search_child_by_name(object_transform_box, 'Rotation z button')

        self._position_x_button.connect('value-changed', self.update_position)
        self._position_y_button.connect('value-changed', self.update_position)
        self._position_z_button.connect('value-changed', self.update_position)
        self._scale_x_button.connect('value-changed', self.update_scale)
        self._scale_y_button.connect('value-changed', self.update_scale)
        self._scale_z_button.connect('value-changed', self.update_scale)
        self._rotation_x_button.connect('value-changed', self.update_rotation)
        self._rotation_y_button.connect('value-changed', self.update_rotation)
        self._rotation_z_button.connect('value-changed', self.update_rotation)

    # pylint: disable=unused-argument
    def update_position(self, user_data) -> None:
        '''
        Atualiza a posição
        '''

        user_call = self._handler_mediator.main_window_handler.user_call
        object_manager = self._handler_mediator.manager_mediator.object_manager
        object_in_focus = object_manager.object_in_focus

        if user_call and object_in_focus is not None:

            diff_x = self._position_x_button.get_value() - object_in_focus.position.x
            diff_y = self._position_y_button.get_value() - object_in_focus.position.y
            diff_z = self._position_z_button.get_value() - object_in_focus.position.z

            object_in_focus.translate(Vector(diff_x, diff_y, diff_z))

            object_index = object_manager.objects.index(object_in_focus)
            object_manager.update_object_info(object_index)

    # pylint: disable=unused-argument
    def update_scale(self, user_data) -> None:
        '''
        Atualiza a escala
        '''

        user_call = self._handler_mediator.main_window_handler.user_call
        object_in_focus = self._handler_mediator.manager_mediator.object_manager.object_in_focus

        if user_call and object_in_focus is not None:

            diff_x = self._scale_x_button.get_value() / object_in_focus.scale.x
            diff_y = self._scale_y_button.get_value() / object_in_focus.scale.y
            diff_z = self._scale_z_button.get_value() / object_in_focus.scale.z

            object_in_focus.rescale(Vector(diff_x, diff_y, diff_z))

    # pylint: disable=unused-argument
    def update_rotation(self, user_data) -> None:
        '''
        Atualiza a rotação
        '''

        user_call = self._handler_mediator.main_window_handler.user_call
        object_in_focus = self._handler_mediator.manager_mediator.object_manager.object_in_focus

        if user_call and object_in_focus is not None:

            diff_x = self._rotation_x_button.get_value() - object_in_focus.rotation.x
            diff_y = self._rotation_y_button.get_value() - object_in_focus.rotation.y
            diff_z = self._rotation_z_button.get_value() - object_in_focus.rotation.z

            object_in_focus.rotate(Vector(diff_x, diff_y, diff_z))

    def update_spin_buttons(self) -> None:
        '''
        Atualiza todos os botões numéricos.
        '''

        object_in_focus = self._handler_mediator.manager_mediator.object_manager.object_in_focus

        self._handler_mediator.main_window_handler.user_call = False
        self._position_x_button.set_value(object_in_focus.position.x)
        self._position_y_button.set_value(object_in_focus.position.y)
        self._position_z_button.set_value(object_in_focus.position.z)
        self._scale_x_button.set_value(object_in_focus.scale.x)
        self._scale_y_button.set_value(object_in_focus.scale.y)
        self._scale_z_button.set_value(object_in_focus.scale.z)
        self._rotation_x_button.set_value(object_in_focus.rotation.x)
        self._rotation_y_button.set_value(object_in_focus.rotation.y)
        self._rotation_z_button.set_value(object_in_focus.rotation.z)
        self._handler_mediator.main_window_handler.user_call = True
