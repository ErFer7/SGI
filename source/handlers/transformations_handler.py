# -*- coding: utf-8 -*-

'''
Módulo para o handler de transformações.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from gi.repository import Gtk

from source.internals.transform import Vector
from source.handlers.handler import Handler

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow


class TransformationsHandler(Handler):

    '''
    Handler de transformações.
    '''

    _rotation_anchor: Vector
    _translate_x_button: Gtk.SpinButton
    _translate_y_button: Gtk.SpinButton
    _translate_z_button: Gtk.SpinButton
    _rescale_x_button: Gtk.SpinButton
    _rescale_y_button: Gtk.SpinButton
    _rescale_z_button: Gtk.SpinButton
    _rotation_button: Gtk.SpinButton
    _rotation_anchor_button: Gtk.Button
    _rotation_anchor_button_x: Gtk.SpinButton
    _rotation_anchor_button_y: Gtk.SpinButton
    _rotation_anchor_button_z: Gtk.SpinButton
    _apply_translation_button: Gtk.Button
    _apply_scaling_button: Gtk.Button
    _apply_rotation_button: Gtk.Button

    def __init__(self, handler_mediator: HandlerMediator, main_window: MainWindow) -> None:
        super().__init__(handler_mediator)

        self._rotation_anchor = Vector(0.0, 0.0, 0.0)

        transformations_box = main_window.transformations_box

        self._translate_x_button = self.search_child_by_name(transformations_box, 'Translate x button')
        self._translate_y_button = self.search_child_by_name(transformations_box, 'Translate y button')
        self._translate_z_button = self.search_child_by_name(transformations_box, 'Translate z button')
        self._rescale_x_button = self.search_child_by_name(transformations_box, 'Rescale x button')
        self._rescale_y_button = self.search_child_by_name(transformations_box, 'Rescale y button')
        self._rescale_z_button = self.search_child_by_name(transformations_box, 'Rescale z button')
        self._rotation_button = self.search_child_by_name(transformations_box, 'Rotation button')
        self._rotation_anchor_button = self.search_child_by_name(transformations_box, 'Rotation anchor button')
        self._rotation_anchor_button_x = self.search_child_by_name(transformations_box, 'Rotation anchor x button')
        self._rotation_anchor_button_y = self.search_child_by_name(transformations_box, 'Rotation anchor y button')
        self._rotation_anchor_button_z = self.search_child_by_name(transformations_box, 'Rotation anchor z button')
        self._apply_translation_button = self.search_child_by_name(transformations_box, 'Apply translation button')
        self._apply_scaling_button = self.search_child_by_name(transformations_box, 'Apply scaling button')
        self._apply_rotation_button = self.search_child_by_name(transformations_box, 'Apply rotation button')

        self._apply_translation_button.connect('clicked', self.translate)
        self._apply_scaling_button.connect('clicked', self.rescale)
        self._apply_rotation_button.connect('clicked', self.rotate)
        self._rotation_anchor_button.connect('clicked', self.change_rotation_anchor)
        self._rotation_anchor_button_x.connect('value-changed', self.update_rotation_anchor)
        self._rotation_anchor_button_y.connect('value-changed', self.update_rotation_anchor)
        self._rotation_anchor_button_z.connect('value-changed', self.update_rotation_anchor)

    def translate(self, _) -> None:
        '''
        Aplica a translação no objeto em foco.
        '''

        object_manager = self._handler_mediator.manager_mediator.object_manager
        object_in_focus = object_manager.object_in_focus

        if object_in_focus is not None:
            translation_x = self._translate_x_button.get_value()
            translation_y = self._translate_y_button.get_value()
            translation_z = self._translate_z_button.get_value()

            object_in_focus.translate(Vector(translation_x, translation_y, translation_z))
            self._handler_mediator.object_transform_handler.update_spin_buttons()
            self.update_rotation_anchor_spin_buttons()

            object_index = object_manager.objects.index(object_in_focus)
            object_manager.update_object_info(object_index)

    def rescale(self, _) -> None:
        '''
        Aplica a escala no objeto em foco.
        '''

        object_in_focus = self._handler_mediator.manager_mediator.object_manager.object_in_focus

        if object_in_focus is not None:
            scale_x = self._rescale_x_button.get_value()
            scale_y = self._rescale_y_button.get_value()
            scale_z = self._rescale_z_button.get_value()

            object_in_focus.rescale(Vector(scale_x, scale_y, scale_z))
            self._handler_mediator.object_transform_handler.update_spin_buttons()
            self.update_rotation_anchor_spin_buttons()

    def rotate(self, _) -> None:
        '''
        Aplica a rotação no objeto em foco.
        '''

        object_in_focus = self._handler_mediator.manager_mediator.object_manager.object_in_focus

        if object_in_focus is not None:
            angle = self._rotation_button.get_value()

            object_in_focus.rotate(Vector(0.0, 0.0, angle), self._rotation_anchor)
            self._handler_mediator.object_transform_handler.update_spin_buttons()
            self.update_rotation_anchor_spin_buttons()

    def change_rotation_anchor(self, _) -> None:
        '''
        Muda a ancoragem da rotação.
        '''

        match self._rotation_anchor_button.get_label():
            case 'Object':
                self._rotation_anchor = Vector(0.0, 0.0, 0.0)
                self._handler_mediator.object_transform_handler.update_spin_buttons()
                self.update_rotation_anchor_spin_buttons()
                self._rotation_anchor_button.set_label('World')
            case 'World':
                self._rotation_anchor.x = self._rotation_anchor_button_x.get_value()
                self._rotation_anchor.y = self._rotation_anchor_button_y.get_value()
                self._rotation_anchor.z = self._rotation_anchor_button_z.get_value()
                self._rotation_anchor_button_x.set_editable(True)
                self._rotation_anchor_button_y.set_editable(True)
                self._rotation_anchor_button_z.set_editable(True)
                self._rotation_anchor_button.set_label('Specified')
            case 'Specified':
                object_in_focus = self._handler_mediator.manager_mediator.object_manager.object_in_focus

                if object_in_focus is not None:
                    self._rotation_anchor = object_in_focus.position
                else:
                    self._rotation_anchor = Vector(0.0, 0.0, 0.0)

                self._rotation_anchor_button_x.set_editable(False)
                self._rotation_anchor_button_y.set_editable(False)
                self._rotation_anchor_button_z.set_editable(False)
                self._handler_mediator.object_transform_handler.update_spin_buttons()
                self.update_rotation_anchor_spin_buttons()
                self._rotation_anchor_button.set_label('Object')

    def update_rotation_anchor(self, _) -> None:
        '''
        Atualiza o ponto de ancoragem da rotação.
        '''

        if self._handler_mediator.main_window_handler.user_call:
            anchor_x = self._rotation_anchor_button_x.get_value()
            anchor_y = self._rotation_anchor_button_y.get_value()
            anchor_z = self._rotation_anchor_button_z.get_value()

            self._rotation_anchor = Vector(anchor_x, anchor_y, anchor_z)

    def update_object_rotation_anchor(self, anchor: Vector) -> None:
        '''
        Atualiza o ponto de ancoragem da rotação do objeto em foco.
        '''

        if self._rotation_anchor_button.get_label() == 'Object':
            self._rotation_anchor = anchor

    def update_rotation_anchor_spin_buttons(self) -> None:
        '''
        Atualiza todos os botões numéricos.
        '''

        self._handler_mediator.main_window_handler.user_call = False
        self._rotation_anchor_button_x.set_value(self._rotation_anchor.x)
        self._rotation_anchor_button_y.set_value(self._rotation_anchor.y)
        self._rotation_anchor_button_z.set_value(self._rotation_anchor.z)
        self._handler_mediator.main_window_handler.user_call = True
