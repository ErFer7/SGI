# -*- coding: utf-8 -*-

'''
Módulo para o editor.
'''

import gi
from source.transform import Vector

from source.wireframe import ObjectType, Object, Point, Line, Triangle, Rectangle, Wireframe

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EditorHandler():

    '''
    Handler dos botões de edição.
    '''

    # Atributos privados
    _main_window: None
    _focus_object: Object
    _temp_coords: list[Vector]
    _mode: ObjectType
    _width: float
    _color: list[float]
    _edges: int
    _rotation_anchor: Vector
    _edges_button: Gtk.SpinButton
    _point_button: Gtk.ToggleButton
    _line_button: Gtk.ToggleButton
    _triangle_button: Gtk.ToggleButton
    _rectangle_button: Gtk.ToggleButton
    _polygon_button: Gtk.ToggleButton
    _width_button: Gtk.SpinButton
    _color_button: Gtk.ColorButton
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
    _user_call_lock: bool

    def __init__(self,
                 main_window,
                 file_button: Gtk.MenuItem,
                 point_button: Gtk.ToggleButton,
                 line_button: Gtk.ToggleButton,
                 triangle_button: Gtk.ToggleButton,
                 rectangle_button: Gtk.ToggleButton,
                 polygon_button: Gtk.ToggleButton,
                 width_button: Gtk.SpinButton,
                 color_button: Gtk.ColorButton,
                 edges_button: Gtk.SpinButton,
                 remove_button: Gtk.Button,
                 position_x_button: Gtk.SpinButton,
                 position_y_button: Gtk.SpinButton,
                 position_z_button: Gtk.SpinButton,
                 scale_x_button: Gtk.SpinButton,
                 scale_y_button: Gtk.SpinButton,
                 scale_z_button: Gtk.SpinButton,
                 rotation_x_button: Gtk.SpinButton,
                 rotation_y_button: Gtk.SpinButton,
                 rotation_z_button: Gtk.SpinButton,
                 translate_x_button: Gtk.SpinButton,
                 translate_y_button: Gtk.SpinButton,
                 translate_z_button: Gtk.SpinButton,
                 apply_translation_button: Gtk.Button,
                 rescale_x_button: Gtk.SpinButton,
                 rescale_y_button: Gtk.SpinButton,
                 rescale_z_button: Gtk.SpinButton,
                 apply_scaling_button: Gtk.Button,
                 rotation_button: Gtk.SpinButton,
                 apply_rotation_button: Gtk.Button,
                 rotation_anchor_button: Gtk.Button,
                 rotation_anchor_button_x: Gtk.SpinButton,
                 rotation_anchor_button_y: Gtk.SpinButton,
                 rotation_anchor_button_z: Gtk.SpinButton) -> None:

        self._main_window = main_window
        self._focus_object = None
        self._temp_coords = []
        self._mode = ObjectType.NULL
        self._width = 1.0
        self._color = [1.0, 1.0, 1.0]
        self._edges = 3
        self._rotation_anchor = None

        self._width_button = width_button
        self._color_button = color_button
        self._edges_button = edges_button
        self._width_button.connect("value-changed", self.set_width)
        self._color_button.connect("color-set", self.set_color)
        self._edges_button.connect("value-changed", self.set_edges)

        self._point_button = point_button
        self._line_button = line_button
        self._triangle_button = triangle_button
        self._rectangle_button = rectangle_button
        self._polygon_button = polygon_button

        self._position_x_button = position_x_button
        self._position_y_button = position_y_button
        self._position_z_button = position_z_button
        self._scale_x_button = scale_x_button
        self._scale_y_button = scale_y_button
        self._scale_z_button = scale_z_button
        self._rotation_x_button = rotation_x_button
        self._rotation_y_button = rotation_y_button
        self._rotation_z_button = rotation_z_button

        self._translate_x_button = translate_x_button
        self._translate_y_button = translate_y_button
        self._translate_z_button = translate_z_button

        self._rescale_x_button = rescale_x_button
        self._rescale_y_button = rescale_y_button
        self._rescale_z_button = rescale_z_button

        self._rotation_button = rotation_button
        self._rotation_anchor_button = rotation_anchor_button
        self._rotation_anchor_button_x = rotation_anchor_button_x
        self._rotation_anchor_button_y = rotation_anchor_button_y
        self._rotation_anchor_button_z = rotation_anchor_button_z

        file_button.connect("select", self.show_explorer)

        self._point_button.connect("toggled", self.set_mode, ObjectType.POINT)
        self._line_button.connect("toggled", self.set_mode, ObjectType.LINE)
        self._triangle_button .connect("toggled", self.set_mode, ObjectType.TRIANGLE)
        self._rectangle_button.connect("toggled", self.set_mode, ObjectType.RECTANGLE)
        self._polygon_button.connect("toggled", self.set_mode, ObjectType.POLYGON)

        remove_button.connect("clicked", self.remove)

        apply_translation_button.connect("clicked", self.translate)
        apply_scaling_button.connect("clicked", self.rescale)
        apply_rotation_button.connect("clicked", self.rotate)
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

        self._user_call_lock = True

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

    def update_toggle_buttons(self, mode: ObjectType) -> None:
        '''
        Atualiza todos os botões de marcação
        '''

        self._user_call_lock = False
        match mode:
            case ObjectType.POINT:
                self._point_button.set_active(False)
            case ObjectType.LINE:
                self._line_button.set_active(False)
            case ObjectType.TRIANGLE:
                self._triangle_button.set_active(False)
            case ObjectType.RECTANGLE:
                self._rectangle_button.set_active(False)
            case ObjectType.POLYGON:
                self._polygon_button.set_active(False)
        self._user_call_lock = True

    def handle_click(self, position: Vector) -> None:
        '''
        Processa um clique no viewport.
        '''

        if self._mode != ObjectType.NULL:

            self._temp_coords.append(position)
            object_completed = False

            if self._mode == ObjectType.POINT and len(self._temp_coords) >= 1:
                self._main_window.display_file_handler.add_object(Point(self._temp_coords[0], "Point", self._color))
                object_completed = True
            elif self._mode == ObjectType.LINE and len(self._temp_coords) >= 2:
                self._main_window.display_file_handler.add_object(
                    Line(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Line",
                        self._color,
                        self._width))
                object_completed = True
            elif self._mode == ObjectType.TRIANGLE and len(self._temp_coords) >= 3:
                self._main_window.display_file_handler.add_object(
                    Triangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        self._temp_coords[2],
                        "Triangle",
                        self._color,
                        self._width))
                object_completed = True
            elif self._mode == ObjectType.RECTANGLE and len(self._temp_coords) >= 2:
                self._main_window.display_file_handler.add_object(
                    Rectangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Rectangle",
                        self._color,
                        self._width))
                object_completed = True
            elif self._mode == ObjectType.POLYGON and len(self._temp_coords) >= self._edges:
                self._main_window.display_file_handler.add_object(
                    Wireframe(
                        self._temp_coords.copy(),
                        "Wireframe",
                        self._color,
                        self._width))
                object_completed = True

            if object_completed:
                self._focus_object = self._main_window.display_file_handler.objects[-1]
                self._rotation_anchor = self._focus_object.position
                self.update_spin_buttons()
                self._temp_coords.clear()

    def set_mode(self, user_data, mode: ObjectType) -> None:
        '''
        Define o modo.
        '''

        if not self._user_call_lock:
            return

        self._focus_object = None

        if self._mode != mode:

            self.update_toggle_buttons(self._mode)
            self._mode = mode
        else:
            self._mode = ObjectType.NULL

        if self._mode == ObjectType.POLYGON:
            self._edges_button.set_editable(True)
        else:
            self._edges_button.set_editable(False)

        self._temp_coords.clear()

    def set_width(self, user_data) -> None:
        '''
        Handler da mudança de tamanho.
        '''

        self._width = self._width_button.get_value()

    def set_color(self, user_data) -> None:
        '''
        Handler da mudança de cor.
        '''

        rgba = self._color_button.get_rgba()
        self._color = (rgba.red, rgba.green, rgba.blue)

    def set_edges(self, user_data) -> None:
        '''
        Handler da mudança da contagem de arestas.
        '''

        self._edges = self._edges_button.get_value_as_int()

    def remove(self, user_data) -> None:
        '''
        Remove um objeto. (Atualmente remove todos)
        '''

        self._main_window.display_file_handler.remove_last()

    def show_explorer(self, user_data) -> None:
        '''
        Mostra o explorador de arquivos.
        '''

        # TODO: Estudar uma maneira de fazer isso funcionar
        raise NotImplementedError

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

            self._focus_object.rotate(angle, self._rotation_anchor)
            self.update_spin_buttons()

    def change_rotation_anchor(self, user_data) -> None:
        '''
        Muda a ancoragem da rotação.
        '''

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

            # diff_x = self._rotation_x_button.get_value() - self._focus_object.rotation.x
            # diff_y = self._rotation_y_button.get_value() - self._focus_object.rotation.y
            diff_z = self._rotation_z_button.get_value() - self._focus_object.rotation.z

            self._focus_object.rotate(diff_z)

    def update_rotation_anchor(self, user_data) -> None:
        '''
        Atualiza o ponto de ancoragem da rotação.
        '''

        if self._user_call_lock:

            anchor_x = self._rotation_anchor_button_x.get_value()
            anchor_y = self._rotation_anchor_button_y.get_value()
            anchor_z = self._rotation_anchor_button_z.get_value()

            self._rotation_anchor = Vector(anchor_x, anchor_y, anchor_z)
