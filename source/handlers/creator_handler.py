# -*- coding: utf-8 -*-

'''
Módulo para o criador.
'''

import gi


gi.require_version('Gtk', '3.0')

# pylint: disable=wrong-import-position
from gi.repository import Gtk # type: ignore

import source.internals.wireframe as wireframe

from source.internals.transform import Vector
from source.managers.object_manager import ObjectManager
from source.handlers.handler_utils import HandlerUtils


class CreatorHandler():

    '''
    Handler dos botões de criação.
    '''

    _point_button: Gtk.ToggleButton
    _line_button: Gtk.ToggleButton
    _triangle_button: Gtk.ToggleButton
    _rectangle_button: Gtk.ToggleButton
    _polygon_button: Gtk.ToggleButton
    _bezier_curve_button: Gtk.ToggleButton
    _spline_curve_button: Gtk.ToggleButton
    _surface_button: Gtk.ToggleButton
    _parallelepiped_button: Gtk.ToggleButton
    _remove_button: Gtk.Button
    _width_button: Gtk.SpinButton
    _color_button: Gtk.ColorButton
    _edges_button: Gtk.SpinButton
    _fill_button: Gtk.CheckButton
    _curve_point_count_button: Gtk.SpinButton
    _curve_step_count_button: Gtk.SpinButton
    _spline_point_count_button: Gtk.SpinButton
    _spline_step_count_button: Gtk.SpinButton
    _closed_spline_button: Gtk.CheckButton
    _surface_step_count_button: Gtk.SpinButton
    _input_x_button: Gtk.SpinButton
    _input_y_button: Gtk.SpinButton
    _input_z_button: Gtk.SpinButton
    _add_point_button: Gtk.Button
    _user_call_lock: bool
    _object_manager: ObjectManager
    _mode: wireframe.ObjectType
    _temp_coords: list[Vector]
    _width: float
    _color: tuple[float, float, float]
    _fill: bool
    _edges: int
    _curve_point_count: int
    _curve_step_count: int
    _spline_point_count: int
    _spline_step_count: int
    _surface_step_count: int
    _closed_spline: bool

    def __init__(self, editor_box: Gtk.Box, object_manager: ObjectManager) -> None:
        self._user_call_lock = True
        self._mode = wireframe.ObjectType.NULL
        self._temp_coords = []
        self._width = 1.0
        self._color = (1.0, 1.0, 1.0)
        self._fill = False
        self._edges = 3
        self._curve_point_count = 4
        self._curve_step_count = 15
        self._spline_point_count = 4
        self._spline_step_count = 10
        self._surface_step_count = 10
        self._closed_spline = False
        self._object_manager = object_manager
        self._point_button = HandlerUtils.search_child_by_name(editor_box, 'Point button')
        self._line_button = HandlerUtils.search_child_by_name(editor_box, 'Line button')
        self._triangle_button = HandlerUtils.search_child_by_name(editor_box, 'Triangle button')
        self._rectangle_button = HandlerUtils.search_child_by_name(editor_box, 'Rectangle button')
        self._polygon_button = HandlerUtils.search_child_by_name(editor_box, 'Polygon button')
        self._bezier_curve_button = HandlerUtils.search_child_by_name(editor_box, 'Bezier curve button')
        self._spline_curve_button = HandlerUtils.search_child_by_name(editor_box, 'Spline curve button')
        self._surface_button = HandlerUtils.search_child_by_name(editor_box, 'Surface button')
        self._parallelepiped_button = HandlerUtils.search_child_by_name(editor_box, 'Parallelepiped button')
        self._remove_button = HandlerUtils.search_child_by_name(editor_box, 'Remove button')
        self._width_button = HandlerUtils.search_child_by_name(editor_box, 'Width button')
        self._color_button = HandlerUtils.search_child_by_name(editor_box, 'Color button')
        self._edges_button = HandlerUtils.search_child_by_name(editor_box, 'Edges button')
        self._fill_button = HandlerUtils.search_child_by_name(editor_box, 'Fill button')
        self._curve_point_count_button = HandlerUtils.search_child_by_name(editor_box, 'Curve point count button')
        self._curve_step_count_button = HandlerUtils.search_child_by_name(editor_box, 'Curve step count button')
        self._spline_point_count_button = HandlerUtils.search_child_by_name(editor_box, 'Spline point count button')
        self._spline_step_count_button = HandlerUtils.search_child_by_name(editor_box, 'Spline step count button')
        self._closed_spline_button = HandlerUtils.search_child_by_name(editor_box, 'Closed spline button')
        self._surface_step_count_button = HandlerUtils.search_child_by_name(editor_box, 'Surface step count button')
        self._input_x_button = HandlerUtils.search_child_by_name(editor_box, 'Input x button')
        self._input_y_button = HandlerUtils.search_child_by_name(editor_box, 'Input y button')
        self._input_z_button = HandlerUtils.search_child_by_name(editor_box, 'Input z button')
        self._add_point_button = HandlerUtils.search_child_by_name(editor_box, 'Add point button')

        self._point_button.connect("toggled", self.set_mode, wireframe.ObjectType.POINT)
        self._line_button.connect("toggled", self.set_mode, wireframe.ObjectType.LINE)
        self._triangle_button .connect("toggled", self.set_mode, wireframe.ObjectType.TRIANGLE)
        self._rectangle_button.connect("toggled", self.set_mode, wireframe.ObjectType.RECTANGLE)
        self._polygon_button.connect("toggled", self.set_mode, wireframe.ObjectType.POLYGON)
        self._bezier_curve_button.connect("toggled", self.set_mode, wireframe.ObjectType.BEZIER_CURVE)
        self._spline_curve_button.connect("toggled", self.set_mode, wireframe.ObjectType.SPLINE_CURVE)
        self._surface_button.connect("toggled", self.set_mode, wireframe.ObjectType.SURFACE)
        self._parallelepiped_button.connect("toggled", self.set_mode, wireframe.ObjectType.PARALLELEPIPED)
        self._remove_button.connect("clicked", self.remove)
        self._width_button.connect("value-changed", self.set_width)
        self._color_button.connect("color-set", self.set_color)
        self._edges_button.connect("value-changed", self.set_edges)
        self._fill_button.connect("toggled", self.set_fill)
        self._curve_point_count_button.connect("value-changed", self.set_curve_point_count)
        self._curve_step_count_button.connect("value-changed", self.set_curve_step_count)
        self._spline_point_count_button.connect("value-changed", self.set_spline_point_count)
        self._spline_step_count_button.connect("value-changed", self.set_spline_step_count)
        self._closed_spline_button.connect("toggled", self.set_closed_spline)
        self._surface_step_count_button.connect("value-changed", self.set_surface_step_count)
        self._add_point_button.connect("clicked", self.add_point, True)

    # pylint: disable=unused-argument
    def set_mode(self, user_data, mode: wireframe.ObjectType) -> None:
        '''
        Define o modo.
        '''

        if not self._user_call_lock:
            return

        self._object_manager.object_in_focus = None

        if self._mode != mode:

            self.update_toggle_buttons(self._mode)
            self._mode = mode
        else:
            self._mode = wireframe.ObjectType.NULL

        self._edges_button.set_editable(False)
        self._curve_point_count_button.set_editable(False)
        self._curve_step_count_button.set_editable(False)
        self._spline_point_count_button.set_editable(False)
        self._spline_step_count_button.set_editable(False)
        self._surface_step_count_button.set_editable(False)

        match self._mode:
            case wireframe.ObjectType.POLYGON:
                self._edges_button.set_editable(True)
            case wireframe.ObjectType.BEZIER_CURVE:
                self._curve_point_count_button.set_editable(True)
                self._curve_step_count_button.set_editable(True)
            case wireframe.ObjectType.SPLINE_CURVE:
                self._spline_point_count_button.set_editable(True)
                self._spline_step_count_button.set_editable(True)
            case wireframe.ObjectType.SURFACE:
                self._surface_step_count_button.set_editable(True)

        self._temp_coords.clear()

    def update_toggle_buttons(self, mode: wireframe.ObjectType) -> None:
        '''
        Atualiza todos os botões de marcação.
        '''

        self._user_call_lock = False
        match mode:
            case wireframe.ObjectType.POINT:
                self._point_button.set_active(False)
            case wireframe.ObjectType.LINE:
                self._line_button.set_active(False)
            case wireframe.ObjectType.TRIANGLE:
                self._triangle_button.set_active(False)
            case wireframe.ObjectType.RECTANGLE:
                self._rectangle_button.set_active(False)
            case wireframe.ObjectType.POLYGON:
                self._polygon_button.set_active(False)
            case wireframe.ObjectType.BEZIER_CURVE:
                self._bezier_curve_button.set_active(False)
            case wireframe.ObjectType.SPLINE_CURVE:
                self._spline_curve_button.set_active(False)
            case wireframe.ObjectType.SURFACE:
                self._surface_button.set_active(False)
            case wireframe.ObjectType.PARALLELEPIPED:
                self._parallelepiped_button.set_active(False)
        self._user_call_lock = True

    # pylint: disable=unused-argument
    def remove(self, user_data) -> None:
        '''
        Remove o último objeto.
        '''

        self._object_manager.remove_last()

    # pylint: disable=unused-argument
    def set_width(self, user_data) -> None:
        '''
        Handler da mudança de tamanho.
        '''

        self._width = self._width_button.get_value()

    # pylint: disable=unused-argument
    def set_color(self, user_data) -> None:
        '''
        Handler da mudança de cor.
        '''

        rgba = self._color_button.get_rgba()
        self._color = (rgba.red, rgba.green, rgba.blue)

    # pylint: disable=unused-argument
    def set_fill(self, user_data) -> None:
        '''
        Handler da definição de preenchimento.
        '''

        self._fill = not self._fill

    # pylint: disable=unused-argument
    def set_edges(self, user_data) -> None:
        '''
        Handler da mudança da contagem de arestas.
        '''

        self._edges = self._edges_button.get_value_as_int()

    # pylint: disable=unused-argument
    def set_curve_point_count(self, user_data) -> None:
        '''
        Handler da mudança da contagem de pontos de controle da curva de Bezier.
        '''

        self._curve_point_count = self._curve_point_count_button.get_value_as_int()

    # pylint: disable=unused-argument
    def set_curve_step_count(self, user_data) -> None:
        '''
        handler da mudança da contagem de passos no processamento de curvas.
        '''

        self._curve_step_count = self._curve_step_count_button.get_value_as_int()

    # pylint: disable=unused-argument
    def set_spline_point_count(self, user_data) -> None:
        '''
        Handler da mudança da contagem de pontos do Spline.
        '''

        self._spline_point_count = self._spline_point_count_button.get_value_as_int()

    # pylint: disable=unused-argument
    def set_spline_step_count(self, user_data) -> None:
        '''
        handler da mudança da contagem de passos no processamento de Splines.
        '''

        self._spline_step_count = self._spline_step_count_button.get_value_as_int()

    # pylint: disable=unused-argument
    def set_closed_spline(self, user_data) -> None:
        '''
        Handler para definir se o Spline é fechado ou não.
        '''

        self._closed_spline = not self._closed_spline

    # pylint: disable=unused-argument
    def set_surface_step_count(self, user_data) -> None:
        '''
        handler da mudança da contagem de passos no processamento de superfícies.
        '''

        self._surface_step_count = self._surface_step_count_button.get_value_as_int()

    def add_point(self, position: Vector, user_data = False) -> None:
        '''
        Processa a adição de um ponto.
        '''

        if user_data is True:
            new_x = self._input_x_button.get_value()
            new_y = self._input_y_button.get_value()
            new_z = self._input_z_button.get_value()

            position = Vector(new_x, new_y, new_z)

        if self._mode != wireframe.ObjectType.NULL:

            self._temp_coords.append(position)
            object_completed = False

            if self._mode == wireframe.ObjectType.POINT and len(self._temp_coords) >= 1:
                self._object_manager.add_object(wireframe.Point(self._temp_coords[0], "Point", self._color))
                object_completed = True
            elif self._mode == wireframe.ObjectType.LINE and len(self._temp_coords) >= 2:
                self._object_manager.add_object(
                    wireframe.Line(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Line",
                        self._color,
                        self._width))
                object_completed = True
            elif self._mode == wireframe.ObjectType.TRIANGLE and len(self._temp_coords) >= 3:
                self._object_manager.add_object(
                    wireframe.Triangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        self._temp_coords[2],
                        "Triangle",
                        self._color,
                        self._width,
                        self._fill))
                object_completed = True
            elif self._mode == wireframe.ObjectType.RECTANGLE and len(self._temp_coords) >= 2:
                self._object_manager.add_object(
                    wireframe.Rectangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Rectangle",
                        self._color,
                        self._width,
                        self._fill))
                object_completed = True
            elif self._mode == wireframe.ObjectType.POLYGON and len(self._temp_coords) >= self._edges:
                self._object_manager.add_object(
                    wireframe.Wireframe2D(
                        self._temp_coords.copy(),
                        "Wireframe",
                        self._color,
                        self._width,
                        wireframe.ObjectType.POLYGON,
                        self._fill))
                object_completed = True
            elif self._mode == wireframe.ObjectType.BEZIER_CURVE:

                self.check_curve_requirements()

                if len(self._temp_coords) >= self._curve_point_count:
                    self._object_manager.add_object(
                        wireframe.BezierCurve(self._temp_coords,
                                    self._curve_step_count,
                                    "Bezier Curve",
                                    self._color,
                                    self._width))
                    object_completed = True
            elif self._mode == wireframe.ObjectType.SPLINE_CURVE and len(self._temp_coords) >= self._spline_point_count:
                self._object_manager.add_object(
                    wireframe.SplineCurve(self._temp_coords,
                                self._fill,
                                self._closed_spline,
                                self._spline_step_count,
                                "Bezier Curve",
                                self._color,
                                self._width))
                object_completed = True
            elif self._mode == wireframe.ObjectType.SURFACE and len(self._temp_coords) >= 16:
                self._object_manager.add_object(
                    wireframe.Surface(self._temp_coords,
                            self._surface_step_count,
                            "Surface",
                            self._color,
                            self._width))
                object_completed = True
            elif self._mode == wireframe.ObjectType.PARALLELEPIPED and len(self._temp_coords) >= 2:
                self._object_manager.add_object(
                    wireframe.Parallelepiped(self._temp_coords[0],
                                    self._temp_coords[1],
                                    "Parallelepiped",
                                    self._color,
                                    self._width))
                object_completed = True

            if object_completed:
                self._object_manager.set_last_as_focus()
                self._rotation_anchor = self._focus_object.position
                self.update_spin_buttons()
                self._temp_coords.clear()

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
