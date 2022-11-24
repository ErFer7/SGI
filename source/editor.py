# -*- coding: utf-8 -*-

'''
Módulo para o editor.
'''

import gi

from source.transform import Vector
from source.wireframe import ObjectType, Object, Point, Line, Triangle, Rectangle, Wireframe, BezierCurve, SplineCurve

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
    _fill: bool
    _curve_point_count: int
    _curve_step_count: int
    _spline_point_count: int
    _spline_step_count: int
    _rotation_anchor: Vector
    _edges_button: Gtk.SpinButton
    _curve_point_count_button: Gtk.SpinButton
    _curve_step_count_button: Gtk.SpinButton
    _spline_point_count_button: Gtk.SpinButton
    _spline_step_count_button: Gtk.SpinButton
    _fill_button: Gtk.CheckButton
    _point_button: Gtk.ToggleButton
    _line_button: Gtk.ToggleButton
    _triangle_button: Gtk.ToggleButton
    _rectangle_button: Gtk.ToggleButton
    _polygon_button: Gtk.ToggleButton
    _bezier_curve_button: Gtk.ToggleButton
    _spline_curve_button: Gtk.ToggleButton
    _closed_spline_button: Gtk.CheckButton
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
    _clipping_method_button: Gtk.ToggleButton
    _user_call_lock: bool

    def __init__(self, main_window) -> None:

        self._main_window = main_window
        self._focus_object = None
        self._temp_coords = []
        self._mode = ObjectType.NULL
        self._width = 1.0
        self._color = [1.0, 1.0, 1.0]
        self._edges = 3
        self._fill = False
        self._curve_point_count = 4
        self._curve_step_count = 15
        self._spline_point_count = 4
        self._spline_step_count = 10
        self._closed_spline = False
        self._rotation_anchor = None
        self._width_button = self._main_window.width_button
        self._color_button = self._main_window.color_button
        self._edges_button = self._main_window.edges_button
        self._fill_button = self._main_window.fill_button
        self._curve_point_count_button = self._main_window.curve_point_count_button
        self._curve_step_count_button = self._main_window.curve_step_count_button
        self._spline_point_count_button = self._main_window.spline_point_count_button
        self._spline_step_count_button = self._main_window.spline_step_count_button
        self._closed_spline_button = self._main_window.closed_spline_button
        self._point_button = self._main_window.point_button
        self._line_button = self._main_window.line_button
        self._triangle_button = self._main_window.triangle_button
        self._rectangle_button = self._main_window.rectangle_button
        self._polygon_button = self._main_window.polygon_button
        self._bezier_curve_button = self._main_window.bezier_curve_button
        self._spline_curve_button = self._main_window.spline_curve_button
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

        self._width_button.connect("value-changed", self.set_width)
        self._color_button.connect("color-set", self.set_color)
        self._edges_button.connect("value-changed", self.set_edges)
        self._fill_button.connect("toggled", self.set_fill)
        self._curve_point_count_button.connect("value-changed", self.set_curve_point_count)
        self._curve_step_count_button.connect("value-changed", self.set_curve_step_count)
        self._spline_point_count_button.connect("value-changed", self.set_spline_point_count)
        self._spline_step_count_button.connect("value-changed", self.set_spline_step_count)
        self._closed_spline_button.connect("toggled", self.set_closed_spline)
        self._main_window.file_button.connect("select", self.show_explorer)
        self._point_button.connect("toggled", self.set_mode, ObjectType.POINT)
        self._line_button.connect("toggled", self.set_mode, ObjectType.LINE)
        self._triangle_button .connect("toggled", self.set_mode, ObjectType.TRIANGLE)
        self._rectangle_button.connect("toggled", self.set_mode, ObjectType.RECTANGLE)
        self._polygon_button.connect("toggled", self.set_mode, ObjectType.POLYGON)
        self._bezier_curve_button.connect("toggled", self.set_mode, ObjectType.BEZIER_CURVE)
        self._spline_curve_button.connect("toggled", self.set_mode, ObjectType.SPLINE_CURVE)
        self._main_window.remove_button.connect("clicked", self.remove)
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
            case ObjectType.BEZIER_CURVE:
                self._bezier_curve_button.set_active(False)
            case ObjectType.SPLINE_CURVE:
                self._spline_curve_button.set_active(False)
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
                        self._width,
                        self._fill))
                object_completed = True
            elif self._mode == ObjectType.RECTANGLE and len(self._temp_coords) >= 2:
                self._main_window.display_file_handler.add_object(
                    Rectangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Rectangle",
                        self._color,
                        self._width,
                        self._fill))
                object_completed = True
            elif self._mode == ObjectType.POLYGON and len(self._temp_coords) >= self._edges:
                self._main_window.display_file_handler.add_object(
                    Wireframe(
                        self._temp_coords.copy(),
                        "Wireframe",
                        self._color,
                        self._width,
                        ObjectType.POLYGON,
                        self._fill))
                object_completed = True
            elif self._mode == ObjectType.BEZIER_CURVE:

                self.check_curve_requirements()

                if len(self._temp_coords) >= self._curve_point_count:
                    self._main_window.display_file_handler.add_object(
                        BezierCurve(self._temp_coords,
                                    self._curve_step_count,
                                    "Bezier Curve",
                                    self._color,
                                    self._width))
                    object_completed = True
            elif self._mode == ObjectType.SPLINE_CURVE and len(self._temp_coords) >= self._spline_point_count:
                self._main_window.display_file_handler.add_object(
                    SplineCurve(self._temp_coords,
                                self._fill,
                                self._closed_spline,
                                self._spline_step_count,
                                "Bezier Curve",
                                self._color,
                                self._width))
                object_completed = True

            if object_completed:
                self._focus_object = self._main_window.display_file_handler.objects[-1]
                self._rotation_anchor = self._focus_object.position
                self.update_spin_buttons()
                self._temp_coords.clear()

    def handle_key_press(self, key: str) -> None:
        '''
        Processa um evento de pressionamento de tecla.
        '''

        match key:
            case 'q':
                self._main_window.viewport_handler.rotate_window(-10)
            case 'e':
                self._main_window.viewport_handler.rotate_window(10)
            case 'w':
                self._main_window.viewport_handler.move_window(Vector(0.0, 10.0, 0.0))
            case 'a':
                self._main_window.viewport_handler.move_window(Vector(-10.0, 0.0, 0.0))
            case 's':
                self._main_window.viewport_handler.move_window(Vector(0.0, -10.0, 0.0))
            case 'd':
                self._main_window.viewport_handler.move_window(Vector(10.0, 0.0, 0.0))
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

        self._edges_button.set_editable(False)
        self._curve_point_count_button.set_editable(False)
        self._curve_step_count_button.set_editable(False)
        self._spline_point_count_button.set_editable(False)
        self._spline_step_count_button.set_editable(False)

        match self._mode:
            case ObjectType.POLYGON:
                self._edges_button.set_editable(True)
            case ObjectType.BEZIER_CURVE:
                self._curve_point_count_button.set_editable(True)
                self._curve_step_count_button.set_editable(True)
            case ObjectType.SPLINE_CURVE:
                self._spline_point_count_button.set_editable(True)
                self._spline_step_count_button.set_editable(True)

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

    def set_fill(self, user_data) -> None:
        '''
        Handler da definição de preenchimento.
        '''

        self._fill = not self._fill

    def set_curve_point_count(self, user_data) -> None:
        '''
        Handler da mudança da contagem de pontos de controle da curva de Bezier.
        '''

        self._curve_point_count = self._curve_point_count_button.get_value_as_int()

    def set_curve_step_count(self, user_data) -> None:
        '''
        handler da mudança da contagem de passos no processamento de curvas.
        '''

        self._curve_step_count = self._curve_step_count_button.get_value_as_int()

    def set_spline_point_count(self, user_data) -> None:
        '''
        Handler da mudança da contagem de pontos do Spline.
        '''

        self._spline_point_count = self._spline_point_count_button.get_value_as_int()

    def set_spline_step_count(self, user_data) -> None:
        '''
        handler da mudança da contagem de passos no processamento de Splines.
        '''

        self._spline_step_count = self._spline_step_count_button.get_value_as_int()

    def set_closed_spline(self, user_data) -> None:
        '''
        Handler para definir se o Spline é fechado ou não.
        '''

        self._closed_spline = not self._closed_spline

    def check_curve_requirements(self) -> None:
        '''
        Verifica se os pontos de controle são colineares.
        '''

        temp_len = len(self._temp_coords)

        if temp_len > 4 and (temp_len - 4) % 3 == 0:

            if self._temp_coords[-4].y == self._temp_coords[-5].y:
                return

            slope_a = (self._temp_coords[-4].y - self._temp_coords[-5].y) / \
                      (self._temp_coords[-4].x - self._temp_coords[-5].x)

            self._temp_coords[-3].y = slope_a * \
                                      (self._temp_coords[-3].x - self._temp_coords[-4].x) + \
                                      self._temp_coords[-4].y

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
            self._main_window.display_file_handler.request_normalization()

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
            self._main_window.display_file_handler.request_normalization()

    def rotate(self, user_data) -> None:
        '''
        Aplica a rotação no objeto em foco.
        '''

        if self._focus_object is not None:

            angle = self._rotation_button.get_value()

            self._focus_object.rotate(angle, self._rotation_anchor)
            self.update_spin_buttons()
            self._main_window.display_file_handler.request_normalization()

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
            self._main_window.display_file_handler.request_normalization()

    def update_scale(self, user_data) -> None:
        '''
        Atualiza a escala
        '''

        if self._user_call_lock and self._focus_object is not None:

            diff_x = self._scale_x_button.get_value() / self._focus_object.scale.x
            diff_y = self._scale_y_button.get_value() / self._focus_object.scale.y
            diff_z = self._scale_z_button.get_value() / self._focus_object.scale.z

            self._focus_object.rescale(Vector(diff_x, diff_y, diff_z))
            self._main_window.display_file_handler.request_normalization()

    def update_rotation(self, user_data) -> None:
        '''
        Atualiza a rotação
        '''

        if self._user_call_lock and self._focus_object is not None:

            # diff_x = self._rotation_x_button.get_value() - self._focus_object.rotation.x
            # diff_y = self._rotation_y_button.get_value() - self._focus_object.rotation.y
            diff_z = self._rotation_z_button.get_value() - self._focus_object.rotation.z

            self._focus_object.rotate(diff_z)
            self._main_window.display_file_handler.request_normalization()

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
