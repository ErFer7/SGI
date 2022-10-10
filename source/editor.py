# -*- coding: utf-8 -*-

'''
Módulo para o editor.
'''

import gi
from source.displayfile import DisplayFileHandler

from source.wireframe import ObjectType, Line, Object, Point, Rectangle, Triangle

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EditorHandler():

    '''
    Handler dos botões de edição.
    '''

    # Atributos privados
    _focus_object: Object
    _temp_coords: list[tuple]
    _mode: ObjectType
    _width: float
    _color: list[float]
    _display_file: DisplayFileHandler  # Referência ao displayfile
    _point_button: Gtk.Button
    _line_button: Gtk.Button
    _triangle_button: Gtk.Button
    _rectangle_button: Gtk.Button
    _polygon_button: Gtk.Button
    _clear_button: Gtk.Button
    _mode_label: Gtk.Label
    _width_button: Gtk.SpinButton
    _color_button: Gtk.ColorButton

    def __init__(self,
                 display_file: DisplayFileHandler,
                 file_button: Gtk.MenuItem,
                 point_button: Gtk.Button,
                 line_button: Gtk.Button,
                 triangle_button: Gtk.Button,
                 retangle_button: Gtk.Button,
                 polygon_button: Gtk.Button,
                 clear_button: Gtk.Button,
                 width_button: Gtk.SpinButton,
                 color_button: Gtk.ColorButton,
                 mode_label: Gtk.Label,
                 remove_button: Gtk.Button) -> None:

        self._focus_object = None
        self._temp_coords = []
        self._mode = ObjectType.NULL
        self._width = 1.0
        self._color = [1.0, 1.0, 1.0]
        self._display_file = display_file

        # Os botões são nescessários para que seja possível desmarcá-los durante uma seleção de modo
        self._point_button = point_button
        self._line_button = line_button
        self._triangle_button = triangle_button
        self._rectangle_button = retangle_button
        self._polygon_button = polygon_button
        self._clear_button = clear_button
        self._width_button = width_button
        self._color_button = color_button
        self._mode_label = mode_label

        file_button.connect("select", self.show_explorer)
        self._width_button.connect("value-changed", self.set_width)
        self._color_button.connect("color-set", self.set_color)
        self._point_button.connect("clicked", self.set_mode, ObjectType.POINT)
        self._line_button.connect("clicked", self.set_mode, ObjectType.LINE)
        self._triangle_button.connect("clicked", self.set_mode, ObjectType.TRIANGLE)
        self._rectangle_button.connect("clicked", self.set_mode, ObjectType.RECTANGLE)
        self._polygon_button.connect("clicked", self.set_mode, ObjectType.POLYGON)
        self._clear_button.connect("clicked", self.set_mode, ObjectType.NULL)
        remove_button.connect("clicked", self.remove)

    def handle_click(self, position: tuple) -> None:
        '''
        Processa um clique no viewport.
        '''

        if self._mode != ObjectType.NULL:

            self._temp_coords.append(position)
            object_completed = False

            if self._mode == ObjectType.POINT and len(self._temp_coords) >= 1:
                self._display_file.add_object(Point(self._temp_coords[0], "Point", self._color))
                object_completed = True
            elif self._mode == ObjectType.LINE and len(self._temp_coords) >= 2:
                self._display_file.add_object(
                    Line(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Line",
                        self._color,
                        self._width))
                object_completed = True
            elif self._mode == ObjectType.TRIANGLE and len(self._temp_coords) >= 3:
                self._display_file.add_object(
                    Triangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        self._temp_coords[2],
                        "Triangle",
                        self._color,
                        self._width))
                object_completed = True
            elif self._mode == ObjectType.RECTANGLE and len(self._temp_coords) >= 2:
                self._display_file.add_object(
                    Rectangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Rectangle",
                        self._color,
                        self._width))
                object_completed = True

            if object_completed:
                self._focus_object = self._display_file.objects[-1]
                self._temp_coords.clear()

    # TODO: Handler para teclas
    def handle_keypress(self) -> None:
        '''
        Processa um aperto de tecla.
        '''

    def set_mode(self, user_data, mode: ObjectType) -> None:
        '''
        Define o modo.
        '''

        self._focus_object = None
        self._mode = mode
        self._temp_coords.clear()

        match self._mode:
            case ObjectType.NULL:
                self._mode_label.set_text("Mode: -")
            case ObjectType.POINT:
                self._mode_label.set_text("Mode: Point")
            case ObjectType.LINE:
                self._mode_label.set_text("Mode: Line")
            case ObjectType.TRIANGLE:
                self._mode_label.set_text("Mode: Triangle")
            case ObjectType.RECTANGLE:
                self._mode_label.set_text("Mode: Rectangle")
            case ObjectType.POLYGON:
                self._mode_label.set_text("Mode: Polygon")
            case _:
                raise Exception("On no '-'")

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

    def remove(self, user_data) -> None:
        '''
        Remove um objeto. (Atualmente remove todos)
        '''

        self._display_file.remove_all()

    def show_explorer(self, user_data) -> None:
        '''
        Mostra o explorador de arquivos.
        '''

        print("Show explorer")
        # TODO: Estudar uma maneira de fazer isso funcionar
