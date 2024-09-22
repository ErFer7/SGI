'''
Módulo para o criador.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from gi.repository import Gtk

from source.handlers.handler import Handler
from source.backend.math.transform import Vector
from source.backend.objects import wireframes_2d
from source.backend.objects import wireframes_3d

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow


class CreatorHandler(Handler):

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
    _mode: wireframes_2d.ObjectType
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

    def __init__(self, handler_mediator: HandlerMediator, main_window: MainWindow) -> None:
        super().__init__(handler_mediator)

        self._mode = wireframes_2d.ObjectType.NULL
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

        creator_box = main_window.creator_box

        self._point_button = self.search_child_by_name(creator_box, 'Point button')
        self._line_button = self.search_child_by_name(creator_box, 'Line button')
        self._triangle_button = self.search_child_by_name(creator_box, 'Triangle button')
        self._rectangle_button = self.search_child_by_name(creator_box, 'Rectangle button')
        self._polygon_button = self.search_child_by_name(creator_box, 'Polygon button')
        self._bezier_curve_button = self.search_child_by_name(creator_box, 'Bezier curve button')
        self._spline_curve_button = self.search_child_by_name(creator_box, 'Spline curve button')
        self._surface_button = self.search_child_by_name(creator_box, 'Surface button')
        self._parallelepiped_button = self.search_child_by_name(creator_box, 'Parallelepiped button')
        self._remove_button = self.search_child_by_name(creator_box, 'Remove button')
        self._width_button = self.search_child_by_name(creator_box, 'Width button')
        self._color_button = self.search_child_by_name(creator_box, 'Color button')
        self._edges_button = self.search_child_by_name(creator_box, 'Edges button')
        self._fill_button = self.search_child_by_name(creator_box, 'Fill button')
        self._curve_point_count_button = self.search_child_by_name(creator_box, 'Curve point count button')
        self._curve_step_count_button = self.search_child_by_name(creator_box, 'Curve step count button')
        self._spline_point_count_button = self.search_child_by_name(creator_box, 'Spline point count button')
        self._spline_step_count_button = self.search_child_by_name(creator_box, 'Spline step count button')
        self._closed_spline_button = self.search_child_by_name(creator_box, 'Closed spline button')
        self._surface_step_count_button = self.search_child_by_name(creator_box, 'Surface step count button')
        self._input_x_button = self.search_child_by_name(creator_box, 'Input x button')
        self._input_y_button = self.search_child_by_name(creator_box, 'Input y button')
        self._input_z_button = self.search_child_by_name(creator_box, 'Input z button')
        self._add_point_button = self.search_child_by_name(creator_box, 'Add point button')

        self._point_button.connect('toggled', self.set_mode, wireframes_2d.ObjectType.POINT)
        self._line_button.connect('toggled', self.set_mode, wireframes_2d.ObjectType.LINE)
        self._triangle_button .connect('toggled', self.set_mode, wireframes_2d.ObjectType.TRIANGLE)
        self._rectangle_button.connect('toggled', self.set_mode, wireframes_2d.ObjectType.RECTANGLE)
        self._polygon_button.connect('toggled', self.set_mode, wireframes_2d.ObjectType.POLYGON)
        self._bezier_curve_button.connect('toggled', self.set_mode, wireframes_2d.ObjectType.BEZIER_CURVE)
        self._spline_curve_button.connect('toggled', self.set_mode, wireframes_2d.ObjectType.SPLINE_CURVE)
        self._surface_button.connect('toggled', self.set_mode, wireframes_2d.ObjectType.SURFACE)
        self._parallelepiped_button.connect('toggled', self.set_mode, wireframes_2d.ObjectType.PARALLELEPIPED)
        self._remove_button.connect('clicked', self.remove)
        self._width_button.connect('value-changed', self.set_width)
        self._color_button.connect('color-set', self.set_color)
        self._edges_button.connect('value-changed', self.set_edges)
        self._fill_button.connect('toggled', self.set_fill)
        self._curve_point_count_button.connect('value-changed', self.set_curve_point_count)
        self._curve_step_count_button.connect('value-changed', self.set_curve_step_count)
        self._spline_point_count_button.connect('value-changed', self.set_spline_point_count)
        self._spline_step_count_button.connect('value-changed', self.set_spline_step_count)
        self._closed_spline_button.connect('toggled', self.set_closed_spline)
        self._surface_step_count_button.connect('value-changed', self.set_surface_step_count)
        self._add_point_button.connect('clicked', self.add_point, True)

    def set_mode(self, _, mode: wireframes_2d.ObjectType) -> None:
        '''
        Define o modo.
        '''

        if not self._handler_mediator.main_window_handler.user_call:
            return

        object_manager = self.handler_mediator.manager_mediator.object_manager
        object_manager.object_in_focus = None

        if self._mode != mode:
            self.update_toggle_buttons(self._mode)
            self._mode = mode
        else:
            self._mode = wireframes_2d.ObjectType.NULL

        self._edges_button.set_editable(False)
        self._curve_point_count_button.set_editable(False)
        self._curve_step_count_button.set_editable(False)
        self._spline_point_count_button.set_editable(False)
        self._spline_step_count_button.set_editable(False)
        self._surface_step_count_button.set_editable(False)

        match self._mode:
            case wireframes_2d.ObjectType.POLYGON:
                self._edges_button.set_editable(True)
            case wireframes_2d.ObjectType.BEZIER_CURVE:
                self._curve_point_count_button.set_editable(True)
                self._curve_step_count_button.set_editable(True)
            case wireframes_2d.ObjectType.SPLINE_CURVE:
                self._spline_point_count_button.set_editable(True)
                self._spline_step_count_button.set_editable(True)
            case wireframes_2d.ObjectType.SURFACE:
                self._surface_step_count_button.set_editable(True)

        self._temp_coords.clear()

    def update_toggle_buttons(self, mode: wireframes_2d.ObjectType) -> None:
        '''
        Atualiza todos os botões de marcação.
        '''

        self._handler_mediator.main_window_handler.user_call = False
        match mode:
            case wireframes_2d.ObjectType.POINT:
                self._point_button.set_active(False)
            case wireframes_2d.ObjectType.LINE:
                self._line_button.set_active(False)
            case wireframes_2d.ObjectType.TRIANGLE:
                self._triangle_button.set_active(False)
            case wireframes_2d.ObjectType.RECTANGLE:
                self._rectangle_button.set_active(False)
            case wireframes_2d.ObjectType.POLYGON:
                self._polygon_button.set_active(False)
            case wireframes_2d.ObjectType.BEZIER_CURVE:
                self._bezier_curve_button.set_active(False)
            case wireframes_2d.ObjectType.SPLINE_CURVE:
                self._spline_curve_button.set_active(False)
            case wireframes_2d.ObjectType.SURFACE:
                self._surface_button.set_active(False)
            case wireframes_2d.ObjectType.PARALLELEPIPED:
                self._parallelepiped_button.set_active(False)
        self._handler_mediator.main_window_handler.user_call = True

    def remove(self, _) -> None:
        '''
        Remove o último objeto.
        '''

        object_manager = self.handler_mediator.manager_mediator.object_manager
        object_manager.remove_last()

    def set_width(self, _) -> None:
        '''
        Handler da mudança de tamanho.
        '''

        self._width = self._width_button.get_value()

    def set_color(self, _) -> None:
        '''
        Handler da mudança de cor.
        '''

        rgba = self._color_button.get_rgba()
        self._color = (rgba.red, rgba.green, rgba.blue)

    def set_fill(self, _) -> None:
        '''
        Handler da definição de preenchimento.
        '''

        self._fill = not self._fill

    def set_edges(self, _) -> None:
        '''
        Handler da mudança da contagem de arestas.
        '''

        self._edges = self._edges_button.get_value_as_int()

    def set_curve_point_count(self, _) -> None:
        '''
        Handler da mudança da contagem de pontos de controle da curva de Bezier.
        '''

        self._curve_point_count = self._curve_point_count_button.get_value_as_int()

    def set_curve_step_count(self, _) -> None:
        '''
        handler da mudança da contagem de passos no processamento de curvas.
        '''

        self._curve_step_count = self._curve_step_count_button.get_value_as_int()

    def set_spline_point_count(self, _) -> None:
        '''
        Handler da mudança da contagem de pontos do Spline.
        '''

        self._spline_point_count = self._spline_point_count_button.get_value_as_int()

    def set_spline_step_count(self, _) -> None:
        '''
        handler da mudança da contagem de passos no processamento de Splines.
        '''

        self._spline_step_count = self._spline_step_count_button.get_value_as_int()

    def set_closed_spline(self, _) -> None:
        '''
        Handler para definir se o Spline é fechado ou não.
        '''

        self._closed_spline = not self._closed_spline

    def set_surface_step_count(self, _) -> None:
        '''
        handler da mudança da contagem de passos no processamento de superfícies.
        '''

        self._surface_step_count = self._surface_step_count_button.get_value_as_int()

    def add_point(self, position: Vector, user_data=False) -> None:
        '''
        Processa a adição de um ponto.
        '''

        if user_data is True:
            new_x = self._input_x_button.get_value()
            new_y = self._input_y_button.get_value()
            new_z = self._input_z_button.get_value()

            position = Vector(new_x, new_y, new_z)

        object_manager = self.handler_mediator.manager_mediator.object_manager

        if self._mode != wireframes_2d.ObjectType.NULL:
            self._temp_coords.append(position)
            object_completed = False

            if self._mode == wireframes_2d.ObjectType.POINT and len(self._temp_coords) >= 1:
                object_manager.add_object(wireframes_2d.Point(self._temp_coords[0], 'Point', self._color))
                object_completed = True
            elif self._mode == wireframes_2d.ObjectType.LINE and len(self._temp_coords) >= 2:
                object_manager.add_object(
                    wireframes_2d.Line(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        'Line',
                        self._color,
                        self._width))
                object_completed = True
            elif self._mode == wireframes_2d.ObjectType.TRIANGLE and len(self._temp_coords) >= 3:
                object_manager.add_object(
                    wireframes_2d.Triangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        self._temp_coords[2],
                        'Triangle',
                        self._color,
                        self._width,
                        self._fill))
                object_completed = True
            elif self._mode == wireframes_2d.ObjectType.RECTANGLE and len(self._temp_coords) >= 2:
                object_manager.add_object(
                    wireframes_2d.Rectangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        'Rectangle',
                        self._color,
                        self._width,
                        self._fill))
                object_completed = True
            elif self._mode == wireframes_2d.ObjectType.POLYGON and len(self._temp_coords) >= self._edges:
                object_manager.add_object(
                    wireframes_2d.Wireframe2D(
                        self._temp_coords.copy(),
                        'Wireframe',
                        self._color,
                        self._width,
                        wireframes_2d.ObjectType.POLYGON,
                        self._fill))
                object_completed = True
            elif self._mode == wireframes_2d.ObjectType.BEZIER_CURVE:
                self.check_curve_requirements()

                if len(self._temp_coords) >= self._curve_point_count:
                    object_manager.add_object(
                        wireframes_2d.BezierCurve(self._temp_coords,
                                              self._curve_step_count,
                                              'Bezier Curve',
                                              self._color,
                                              self._width))
                    object_completed = True
            elif self._mode == wireframes_2d.ObjectType.SPLINE_CURVE and len(self._temp_coords) >= self._spline_point_count:
                object_manager.add_object(
                    wireframes_2d.SplineCurve(self._temp_coords,
                                          self._fill,
                                          self._closed_spline,
                                          self._spline_step_count,
                                          'Bezier Curve',
                                          self._color,
                                          self._width))
                object_completed = True
            elif self._mode == wireframes_2d.ObjectType.SURFACE and len(self._temp_coords) >= 16:
                object_manager.add_object(
                    wireframes_3d.Surface(self._temp_coords,
                                      self._surface_step_count,
                                      'Surface',
                                      self._color,
                                      self._width))
                object_completed = True
            elif self._mode == wireframes_2d.ObjectType.PARALLELEPIPED and len(self._temp_coords) >= 2:
                object_manager.add_object(
                    wireframes_3d.Parallelepiped(self._temp_coords[0],
                                             self._temp_coords[1],
                                             'Parallelepiped',
                                             self._color,
                                             self._width))
                object_completed = True

            if object_completed:
                object_manager.set_last_as_focus()

                anchor = self._handler_mediator.manager_mediator.object_manager.object_in_focus.position

                self._handler_mediator.transformations_handler.update_object_rotation_anchor(anchor)
                self._handler_mediator.object_transform_handler.update_spin_buttons()
                self._handler_mediator.transformations_handler.update_rotation_anchor_spin_buttons()
                self._temp_coords.clear()

    def check_curve_requirements(self) -> None:
        '''
        Verifica se os pontos de controle são colineares.
        '''

        temp_len = len(self._temp_coords)

        if temp_len > 4 and (temp_len - 4) % 3 == 0:
            if self._temp_coords[-4].y == self._temp_coords[-5].y:
                return

            diff_y = self._temp_coords[-4].y - self._temp_coords[-5].y
            diff_x = self._temp_coords[-4].x - self._temp_coords[-5].x

            try:
                slope_a = diff_y / diff_x
            except ZeroDivisionError:
                return

            diff_middle_x = self._temp_coords[-3].x - self._temp_coords[-4].x
            self._temp_coords[-3].y = slope_a * diff_middle_x + self._temp_coords[-4].y
