# -*- coding: utf-8 -*-

'''
Módulo para o editor.
'''

import gi

from source.internals.transform import Vector
from source.internals.wireframe import *  # Não é o ideal, mas não temos muito tempo

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EditorHandler():

    '''
    Handler dos botões de edição.
    '''

    # Atributos privados
    _main_window: None
    _rotation_anchor: Vector
    _position_x_button: Gtk.SpinButton
    _position_y_button: Gtk.SpinButton
    _position_z_button: Gtk.SpinButton
    _scale_x_button: Gtk.SpinButton
    _scale_y_button: Gtk.SpinButton
    _scale_z_button: Gtk.SpinButton
    _rotation_x_button: Gtk.SpinButton
    _rotation_y_button: Gtk.SpinButton
    _rotation_z_button: Gtk.SpinButton
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
    _clipping_method_button: Gtk.ToggleButton
    _window_movement_magnitude: float

    def __init__(self, main_window) -> None:

        self._main_window = main_window
        self._rotation_anchor = None
        self._add_point_button = self._main_window.add_point_button
        self._position_x_button = self._main_window.position_x_button
        self._position_y_button = self._main_window.position_y_button
        self._position_z_button = self._main_window.position_z_button
        self._scale_x_button = self._main_window.scale_x_button
        self._scale_y_button = self._main_window.scale_y_button
        self._scale_z_button = self._main_window.scale_z_button
        self._rotation_x_button = self._main_window.rotation_x_button
        self._rotation_y_button = self._main_window.rotation_y_button
        self._rotation_z_button = self._main_window.rotation_z_button
        self._translate_x_button = self._main_window.translate_x_button
        self._translate_y_button = self._main_window.translate_y_button
        self._translate_z_button = self._main_window.translate_z_button
        self._rescale_x_button = self._main_window.rescale_x_button
        self._rescale_y_button = self._main_window.rescale_y_button
        self._rescale_z_button = self._main_window.rescale_z_button
        self._rotation_button = self._main_window.rotation_button
        self._rotation_anchor_button = self._main_window.rotation_anchor_button
        self._rotation_anchor_button_x = self._main_window.rotation_anchor_button_x
        self._rotation_anchor_button_y = self._main_window.rotation_anchor_button_y
        self._rotation_anchor_button_z = self._main_window.rotation_anchor_button_z
        self._clipping_method_button = self._main_window.clipping_method_button

        self._main_window.apply_translation_button.connect("clicked", self.translate)
        self._main_window.apply_scaling_button.connect("clicked", self.rescale)
        self._main_window.apply_rotation_button.connect("clicked", self.rotate)
        self._rotation_anchor_button.connect("clicked", self.change_rotation_anchor)
        self._position_x_button.connect("value-changed", self.update_position)
        self._position_y_button.connect("value-changed", self.update_position)
        self._position_z_button.connect("value-changed", self.update_position)
        self._scale_x_button.connect("value-changed", self.update_scale)
        self._scale_y_button.connect("value-changed", self.update_scale)
        self._scale_z_button.connect("value-changed", self.update_scale)
        self._rotation_x_button.connect("value-changed", self.update_rotation)
        self._rotation_y_button.connect("value-changed", self.update_rotation)
        self._rotation_z_button.connect("value-changed", self.update_rotation)
        self._rotation_anchor_button_x.connect("value-changed", self.update_rotation_anchor)
        self._rotation_anchor_button_y.connect("value-changed", self.update_rotation_anchor)
        self._rotation_anchor_button_z.connect("value-changed", self.update_rotation_anchor)
        self._clipping_method_button.connect("toggled", self.toggle_clipping_method)

        self._user_call_lock = True
        self._window_movement_magnitude = 10.0

    def update_spin_buttons(self) -> None:
        '''
        Atualiza todos os botões numéricos.
        '''

        self._user_call_lock = False
        self._position_x_button.set_value(self._focus_object.position.x)
        self._position_y_button.set_value(self._focus_object.position.y)
        self._position_z_button.set_value(self._focus_object.position.z)
        self._scale_x_button.set_value(self._focus_object.scale.x)
        self._scale_y_button.set_value(self._focus_object.scale.y)
        self._scale_z_button.set_value(self._focus_object.scale.z)
        self._rotation_x_button.set_value(self._focus_object.rotation.x)
        self._rotation_y_button.set_value(self._focus_object.rotation.y)
        self._rotation_z_button.set_value(self._focus_object.rotation.z)
        self._rotation_anchor_button_x.set_value(self._rotation_anchor.x)
        self._rotation_anchor_button_y.set_value(self._rotation_anchor.y)
        self._rotation_anchor_button_z.set_value(self._rotation_anchor.z)
        self._user_call_lock = True

    def handle_key_press(self, key: str) -> None:
        '''
        Processa um evento de pressionamento de tecla.
        '''

        movement_magnitude = self._window_movement_magnitude

        if key.isupper():
            movement_magnitude *= 5

        key = key.lower()

        match key:
            case 'q':
                self._main_window.viewport_handler.rotate_window(Vector(0.0, 0.0, -movement_magnitude))
            case 'e':
                self._main_window.viewport_handler.rotate_window(Vector(0.0, 0.0, movement_magnitude))
            case 'w':
                self._main_window.viewport_handler.move_window(Vector(0.0, movement_magnitude, 0.0))
            case 'a':
                self._main_window.viewport_handler.move_window(Vector(-movement_magnitude, 0.0, 0.0))
            case 's':
                self._main_window.viewport_handler.move_window(Vector(0.0, -movement_magnitude, 0.0))
            case 'd':
                self._main_window.viewport_handler.move_window(Vector(movement_magnitude, 0.0, 0.0))
            case 'f':
                self._main_window.viewport_handler.move_window(Vector(0.0, 0.0, movement_magnitude))
            case 'g':
                self._main_window.viewport_handler.move_window(Vector(0.0, 0.0, -movement_magnitude))
            case 'h':
                self._main_window.viewport_handler.rotate_window(Vector(-movement_magnitude, 0.0, 0.0))
            case 'j':
                self._main_window.viewport_handler.rotate_window(Vector(movement_magnitude, 0.0, 0.0))
            case 'k':
                self._main_window.viewport_handler.rotate_window(Vector(0.0, -movement_magnitude, 0.0))
            case 'l':
                self._main_window.viewport_handler.rotate_window(Vector(0.0, movement_magnitude, 0.0))
            case 'r':
                self._main_window.viewport_handler.reset_window_position()
            case 't':
                self._main_window.viewport_handler.reset_window_rotation()
            case 'z':
                self._main_window.viewport_handler.reescale_window(Vector(1.1, 1.1, 1.0))
            case 'c':
                self._main_window.viewport_handler.reescale_window(Vector(0.9, 0.9, 1.0))
            case 'y':
                self._main_window.viewport_handler.reset_window_scale()
            case _:
                pass

    def translate(self, user_data) -> None:
        '''
        Aplica a translação no objeto em foco.
        '''

        if self._focus_object is not None:

            translation_x = self._translate_x_button.get_value()
            translation_y = self._translate_y_button.get_value()
            translation_z = self._translate_z_button.get_value()

            self._focus_object.translate(Vector(translation_x, translation_y, translation_z))
            self.update_spin_buttons()

            object_index = self._main_window.display_file_handler.objects.index(self._focus_object)
            self._main_window.display_file_handler.update_object_info(object_index)

    def rescale(self, user_data) -> None:
        '''
        Aplica a escala no objeto em foco.
        '''

        if self._focus_object is not None:

            scale_x = self._rescale_x_button.get_value()
            scale_y = self._rescale_y_button.get_value()
            scale_z = self._rescale_z_button.get_value()

            self._focus_object.rescale(Vector(scale_x, scale_y, scale_z))
            self.update_spin_buttons()

    def rotate(self, user_data) -> None:
        '''
        Aplica a rotação no objeto em foco.
        '''

        if self._focus_object is not None:

            angle = self._rotation_button.get_value()

            self._focus_object.rotate(Vector(0.0, 0.0, angle), self._rotation_anchor)
            self.update_spin_buttons()

    def change_rotation_anchor(self, user_data) -> None:
        '''
        Muda a ancoragem da rotação.
        '''

        # TODO: Corrigir o bug da ancoragem incorreta quando um novo objeto é adicionado

        match self._rotation_anchor_button.get_label():
            case "Object":

                self._rotation_anchor = Vector(0.0, 0.0, 0.0)
                self.update_spin_buttons()
                self._rotation_anchor_button.set_label("World")
            case "World":

                self._rotation_anchor.x = self._rotation_anchor_button_x.get_value()
                self._rotation_anchor.y = self._rotation_anchor_button_y.get_value()
                self._rotation_anchor.z = self._rotation_anchor_button_z.get_value()
                self._rotation_anchor_button_x.set_editable(True)
                self._rotation_anchor_button_y.set_editable(True)
                self._rotation_anchor_button_z.set_editable(True)
                self._rotation_anchor_button.set_label("Specified")
            case "Specified":

                if self._focus_object is not None:
                    self._rotation_anchor = self._focus_object.position
                else:
                    self._rotation_anchor = Vector(0.0, 0.0, 0.0)

                self._rotation_anchor_button_x.set_editable(False)
                self._rotation_anchor_button_y.set_editable(False)
                self._rotation_anchor_button_z.set_editable(False)
                self.update_spin_buttons()
                self._rotation_anchor_button.set_label("Object")

    def update_position(self, user_data) -> None:
        '''
        Atualiza a posição
        '''

        if self._user_call_lock and self._focus_object is not None:

            diff_x = self._position_x_button.get_value() - self._focus_object.position.x
            diff_y = self._position_y_button.get_value() - self._focus_object.position.y
            diff_z = self._position_z_button.get_value() - self._focus_object.position.z

            self._focus_object.translate(Vector(diff_x, diff_y, diff_z))

            object_index = self._main_window.display_file_handler.objects.index(self._focus_object)
            self._main_window.display_file_handler.update_object_info(object_index)

    def update_scale(self, user_data) -> None:
        '''
        Atualiza a escala
        '''

        if self._user_call_lock and self._focus_object is not None:

            diff_x = self._scale_x_button.get_value() / self._focus_object.scale.x
            diff_y = self._scale_y_button.get_value() / self._focus_object.scale.y
            diff_z = self._scale_z_button.get_value() / self._focus_object.scale.z

            self._focus_object.rescale(Vector(diff_x, diff_y, diff_z))

    def update_rotation(self, user_data) -> None:
        '''
        Atualiza a rotação
        '''

        if self._user_call_lock and self._focus_object is not None:

            diff_x = self._rotation_x_button.get_value() - self._focus_object.rotation.x
            diff_y = self._rotation_y_button.get_value() - self._focus_object.rotation.y
            diff_z = self._rotation_z_button.get_value() - self._focus_object.rotation.z

            self._focus_object.rotate(Vector(diff_x, diff_y, diff_z))

    def update_rotation_anchor(self, user_data) -> None:
        '''
        Atualiza o ponto de ancoragem da rotação.
        '''

        if self._user_call_lock:

            anchor_x = self._rotation_anchor_button_x.get_value()
            anchor_y = self._rotation_anchor_button_y.get_value()
            anchor_z = self._rotation_anchor_button_z.get_value()

            self._rotation_anchor = Vector(anchor_x, anchor_y, anchor_z)

    def toggle_clipping_method(self, user_data) -> None:
        '''
        Muda o método de clipping.
        '''

        self._main_window.viewport_handler.change_clipping_method()

        if self._clipping_method_button.get_label() == "Liang-Barsky":
            self._clipping_method_button.set_label("Cohen-Sutherland")
        else:
            self._clipping_method_button.set_label("Liang-Barsky")
