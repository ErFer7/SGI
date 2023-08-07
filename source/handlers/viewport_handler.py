# -*- coding: utf-8 -*-

'''
Módulo para o handler do viewport.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

import gi

gi.require_version('Gtk', '3.0')

# pylint: disable=wrong-import-position
from gi.repository import Gtk, Gdk # type: ignore

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow

from source.handlers.handler import Handler
from source.internals.transform import Vector


class ViewportHandler(Handler):

    '''
    Handler do viewport.
    '''

    _window_movement_magnitude: float
    _drag_coord: Vector | None
    _viewport_drawing_area: Gtk.DrawingArea

    def __init__(self, handler_mediator: HandlerMediator, main_window: MainWindow) -> None:
        super().__init__(handler_mediator)

        self._window_movement_magnitude = 10.0
        self._drag_coord = None

        self._viewport_drawing_area = main_window.viewport_drawing_area

        self._viewport_drawing_area.connect("draw", self.on_draw)
        self._viewport_drawing_area.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self._viewport_drawing_area.connect("button-press-event", self.on_button_press)
        self._viewport_drawing_area.connect("motion-notify-event", self.on_mouse_motion)
        self._viewport_drawing_area.connect("button-release-event", self.on_button_release)
        self._viewport_drawing_area.connect("scroll-event", self.on_scroll)
        self._viewport_drawing_area.connect("size-allocate", self.on_size_allocate)

    def on_draw(self, area, context) -> None:
        '''
        Método para a renderização.
        '''

        self._handler_mediator.manager_mediator.viewport_manager.draw_frame(area, context)  # type: ignore
        self._viewport_drawing_area.queue_draw()

    def handle_key_press(self, key: str) -> None:
        '''
        Processa um evento de pressionamento de tecla.
        '''

        movement_magnitude = self._window_movement_magnitude

        if key.isupper():
            movement_magnitude *= 5

        key = key.lower()

        viewport_manager = self._handler_mediator.manager_mediator.viewport_manager  # type: ignore

        match key:
            case 'q':
                viewport_manager.rotate_window(Vector(0.0, 0.0, -movement_magnitude))  # type: ignore
            case 'e':
                viewport_manager.rotate_window(Vector(0.0, 0.0, movement_magnitude))  # type: ignore
            case 'w':
                viewport_manager.move_window(Vector(0.0, movement_magnitude, 0.0))  # type: ignore
            case 'a':
                viewport_manager.move_window(Vector(-movement_magnitude, 0.0, 0.0))  # type: ignore
            case 's':
                viewport_manager.move_window(Vector(0.0, -movement_magnitude, 0.0))  # type: ignore
            case 'd':
                viewport_manager.move_window(Vector(movement_magnitude, 0.0, 0.0))  # type: ignore
            case 'f':
                viewport_manager.move_window(Vector(0.0, 0.0, movement_magnitude))  # type: ignore
            case 'g':
                viewport_manager.move_window(Vector(0.0, 0.0, -movement_magnitude))  # type: ignore
            case 'h':
                viewport_manager.rotate_window(Vector(-movement_magnitude, 0.0, 0.0))  # type: ignore
            case 'j':
                viewport_manager.rotate_window(Vector(movement_magnitude, 0.0, 0.0))  # type: ignore
            case 'k':
                viewport_manager.rotate_window(Vector(0.0, -movement_magnitude, 0.0))  # type: ignore
            case 'l':
                viewport_manager.rotate_window(Vector(0.0, movement_magnitude, 0.0))  # type: ignore
            case 'r':
                viewport_manager.reset_window_position()  # type: ignore
            case 't':
                viewport_manager.reset_window_rotation()  # type: ignore
            case 'z':
                viewport_manager.reescale_window(Vector(1.1, 1.1, 1.0))  # type: ignore
            case 'c':
                viewport_manager.reescale_window(Vector(0.9, 0.9, 1.0))  # type: ignore
            case 'y':
                viewport_manager.reset_window_scale()  # type: ignore
            case _:
                pass

    def on_button_press(self, widget, event) -> None:
        '''
        Evento de clique.
        '''

        position = Vector(event.x, event.y)

        if event.button == 1:
            self._handler_mediator.creator_handler.add_point(self.screen_to_world(position))  # type: ignore
        elif event.button == 2:
            self._drag_coord = position

    def on_mouse_motion(self, widget, event):
        '''
        Evento de movimento.
        '''

        if self._drag_coord is not None:

            position = Vector(event.x, event.y)
            diff = self._drag_coord - position
            diff.y = -diff.y
            diff *= self._window.scale.x
            self.move_window(diff)
            self._drag_coord = position

    def on_button_release(self, widget, event) -> None:
        '''
        Evento de liberação do mouse.
        '''

        if event.button == 2:
            self._drag_coord = None

    def on_scroll(self, widget, event) -> None:
        '''
        Evento de rolagem:
        '''

        direction = event.get_scroll_deltas()[2]
        viewport_manager = self._handler_mediator.manager_mediator.viewport_manager  # type: ignore

        if direction > 0:
            viewport_manager.rescale(Vector(1.03, 1.03, 1.0))  # type: ignore
        else:
            viewport_manager.rescale(Vector(0.97, 0.97, 1.0))  # type: ignore

    def on_size_allocate(self, allocation, user_data):
        '''
        Evento de alocação.
        '''

        self._handler_mediator.manager_mediator.viewport_manager.reset_window_scale()  # type: ignore

        # TODO: Achar maneira melhor de atualizar o tamanho da tela.

        # self._window.rescale(Vector(user_data.width / (self._window.extension.x - self._window.origin.x),
        #                             user_data.height / (self._window.extension.y - self._window.origin.y),
        #                             1.0))
