# -*- coding: utf-8 -*-

'''
Módulo para o handler do viewport.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from gi.repository import Gtk, Gdk

from source.internals.vector import Vector
from source.handlers.handler import Handler

if TYPE_CHECKING:
    from source.handlers.handler_mediator import HandlerMediator
    from source.handlers.main_window import MainWindow


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

        self._viewport_drawing_area.connect('draw', self.on_draw)
        self._viewport_drawing_area.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self._viewport_drawing_area.connect('button-press-event', self.on_button_press)
        self._viewport_drawing_area.connect('motion-notify-event', self.on_mouse_motion)
        self._viewport_drawing_area.connect('button-release-event', self.on_button_release)
        self._viewport_drawing_area.connect('scroll-event', self.on_scroll)
        self._viewport_drawing_area.connect('size-allocate', self.on_size_allocate)

    def on_draw(self, area, context) -> None:
        '''
        Método para a renderização.
        '''

        width, height = area.get_allocated_width(), area.get_allocated_height()

        self._handler_mediator.manager_mediator.viewport_manager.draw_frame(area, context, width, height)
        self._viewport_drawing_area.queue_draw()

    def handle_key_press(self, key: str) -> None:
        '''
        Processa um evento de pressionamento de tecla.
        '''

        movement_magnitude = self._window_movement_magnitude

        if key.isupper():
            movement_magnitude *= 5

        key = key.lower()

        viewport_manager = self._handler_mediator.manager_mediator.viewport_manager

        match key:
            case 'q':
                viewport_manager.rotate_window(Vector(0.0, 0.0, -movement_magnitude))
            case 'e':
                viewport_manager.rotate_window(Vector(0.0, 0.0, movement_magnitude))
            case 'w':
                viewport_manager.move_window(Vector(0.0, movement_magnitude, 0.0))
            case 'a':
                viewport_manager.move_window(Vector(-movement_magnitude, 0.0, 0.0))
            case 's':
                viewport_manager.move_window(Vector(0.0, -movement_magnitude, 0.0))
            case 'd':
                viewport_manager.move_window(Vector(movement_magnitude, 0.0, 0.0))
            case 'f':
                viewport_manager.move_window(Vector(0.0, 0.0, movement_magnitude))
            case 'g':
                viewport_manager.move_window(Vector(0.0, 0.0, -movement_magnitude))
            case 'h':
                viewport_manager.rotate_window(Vector(-movement_magnitude, 0.0, 0.0))
            case 'j':
                viewport_manager.rotate_window(Vector(movement_magnitude, 0.0, 0.0))
            case 'k':
                viewport_manager.rotate_window(Vector(0.0, -movement_magnitude, 0.0))
            case 'l':
                viewport_manager.rotate_window(Vector(0.0, movement_magnitude, 0.0))
            case 'r':
                viewport_manager.reset_window_position()
            case 't':
                viewport_manager.reset_window_rotation()
            case 'z':
                viewport_manager.reescale_window(Vector(1.1, 1.1, 1.0))
            case 'c':
                viewport_manager.reescale_window(Vector(0.9, 0.9, 1.0))
            case 'y':
                viewport_manager.reset_window_scale()
            case _:
                pass

    def on_button_press(self, widget, event) -> None:
        '''
        Evento de clique.
        '''

        position = Vector(event.x, event.y)
        viewport_manager = self._handler_mediator.manager_mediator.viewport_manager

        width, height = widget.get_allocated_width(), widget.get_allocated_height()

        if event.button == 1:
            self._handler_mediator.creator_handler.add_point(viewport_manager.screen_to_world(position,
                                                                                              width,
                                                                                              height))
        elif event.button == 2:
            self._drag_coord = position

    def on_mouse_motion(self, _, event):
        '''
        Evento de movimento.
        '''

        if self._drag_coord is not None:
            viewport_manager = self._handler_mediator.manager_mediator.viewport_manager
            position = Vector(event.x, event.y)
            diff = self._drag_coord - position
            diff.y = -diff.y
            diff *= viewport_manager.window.scale.x

            viewport_manager.move_window(diff)

            self._drag_coord = position

    def on_button_release(self, _, event) -> None:
        '''
        Evento de liberação do mouse.
        '''

        if event.button == 2:
            self._drag_coord = None

    def on_scroll(self, _, event) -> None:
        '''
        Evento de rolagem:
        '''

        direction = event.get_scroll_deltas()[2]
        viewport_manager = self._handler_mediator.manager_mediator.viewport_manager

        if direction > 0:
            viewport_manager.reescale_window(Vector(1.03, 1.03, 1.0))
        else:
            viewport_manager.reescale_window(Vector(0.97, 0.97, 1.0))

    def on_size_allocate(self, _, user_data):
        '''
        Evento de alocação.
        '''

        self._handler_mediator.manager_mediator.viewport_manager.resize_window(Vector(user_data.width,
                                                                                      user_data.height,
                                                                                      1.0))
