'''
Neste módulo estão definidos os funcionamentos do viewport.
'''

from __future__ import annotations
from typing import TYPE_CHECKING

from source.backend.math.vector import Vector
from source.backend.objects.window import Window
from source.backend.rendering.clipper import Clipper
from source.backend.rendering.frame_generator import FrameGenerator
from source.managers.manager import Manager

if TYPE_CHECKING:
    from source.managers.manager_mediator import ManagerMediator


class ViewportManager(Manager):

    '''
    Definição do viewport, este viewport é um handler para um widget DrawingArea.
    '''

    _bg_color: tuple
    _window: Window
    _viewport_padding: Vector
    _clipper: Clipper

    def __init__(self,
                 manager_mediator: ManagerMediator,
                 viewport_padding: Vector = Vector(0.0, 0.0, 0.0),
                 bg_color: tuple = (0, 0, 0)) -> None:
        super().__init__(manager_mediator)

        self._bg_color = bg_color
        self._window = Window(Vector(-500.0, -500.0),
                              Vector(500.0, 500.0),
                              Vector(0.0, 0.0, -500.0),
                              (0.5, 0.0, 0.5),
                              2.0)
        self._viewport_padding = viewport_padding
        self._clipper = Clipper()

    @property
    def window(self) -> Window:
        '''
        Retorna a janela do viewport.
        '''

        return self._window

    def world_to_screen(self, coord: Vector, screen_width: int, screen_height: int) -> Vector:
        '''
        Converte a coordenada de mundo para uma coordenada de tela.
        '''

        origin = self._window.normalized_origin - self._viewport_padding
        extension = self._window.normalized_extension + self._viewport_padding

        x_s = ((coord.x - origin.x) / (extension.x - origin.x)) * screen_width
        y_s = (1 - (coord.y - origin.y) / (extension.y - origin.y)) * screen_height

        return Vector(x_s, y_s)

    def world_line_to_screen(self, line: list[Vector], screen_width: int, screen_height: int) -> tuple[Vector]:
        '''
        Converte uma linha no mundo para uma linha na tela.
        '''

        return (self.world_to_screen(line[0], screen_width, screen_height),
                self.world_to_screen(line[1], screen_width, screen_height))

    def screen_to_world(self, coord: Vector, screen_width: int, screen_height: int) -> Vector:
        '''
        Converte a coordenada de tela para uma coordenada de mundo.
        '''

        origin = self._window.origin - self._viewport_padding
        extension = self._window.extension + self._viewport_padding

        x_w = (coord.x / screen_width) * (extension.x - origin.x) + origin.x
        y_w = (1.0 - (coord.y / screen_height)) * (extension.y - origin.y) + origin.y

        return Vector(x_w, y_w)

    def draw_frame(self, area, context, screen_width: int, screen_height: int) -> None:
        '''
        Método para a renderização.
        '''

        # Preenche o fundo
        context.set_source_rgb(self._bg_color[0], self._bg_color[1], self._bg_color[2])
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        FrameGenerator.generate_frame(self._window, self._manager_mediator.object_manager.objects)

        # Renderiza todos os objetos
        for obj in self._manager_mediator.object_manager.objects + [self._window]:
            clipped_lines = []

            if obj != self._window:
                clipped_lines = self._clipper.clip(self._window, obj)
            else:
                clipped_lines = obj.vector_lines

            screen_lines = list(map(lambda x: self.world_line_to_screen(x, screen_width, screen_height),
                                    clipped_lines))
            color = obj.color
            line_width = obj.line_width

            # Define cor e largura do pincel
            context.new_path()
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)

            if obj.fill and len(screen_lines) > 0:
                context.move_to(screen_lines[0][0].x, screen_lines[0][0].y)

            for line in screen_lines:
                if obj.fill:
                    context.line_to(line[1].x, line[1].y)
                else:
                    context.move_to(line[0].x, line[0].y)
                    context.line_to(line[1].x, line[1].y)
                    context.stroke()

            context.close_path()

            if obj.fill:
                context.fill()

    def move_window(self, direction: Vector) -> None:
        '''
        Move a window.
        '''

        self._window.translate(direction)

    def reset_window_position(self) -> None:
        '''
        Redefine a posição da window.
        '''

        self._window.translate(-self._window.position)

    def rotate_window(self, rotation: Vector) -> None:
        '''
        Rotaciona a window.
        '''

        self._window.rotate(rotation)

    def reset_window_rotation(self) -> None:
        '''
        Redefine a rotação da window.
        '''

        self._window.rotate(Vector(0.0, 0.0, -self._window.rotation.z))
        self._window.rotate(Vector(0.0, -self._window.rotation.y, 0.0))
        self._window.rotate(Vector(-self._window.rotation.x, 0.0, 0.0))

    def reescale_window(self, scale: Vector) -> None:
        '''
        Reescala a window.
        '''

        self._window.rescale(scale)

    def reset_window_scale(self) -> None:
        '''
        Redefine a escala da window.
        '''

        diff_x = 1.0 / self._window.scale.x
        diff_y = 1.0 / self._window.scale.y
        diff_z = 1.0 / self._window.scale.z

        self._window.rescale(Vector(diff_x, diff_y, diff_z))

    def resize_window(self, extension: Vector) -> None:
        '''
        Redefine a extensão da window.
        '''

        diff_x = extension.x / self._window.scale.x
        diff_y = extension.y / self._window.scale.y
        diff_z = extension.z / self._window.scale.z

        self._window.rescale(Vector(diff_x, diff_y, diff_z))

    def toggle_clipping_method(self) -> None:
        '''
        Muda o método de clipping.
        '''

        self._clipper.toggle_clipping_method()
