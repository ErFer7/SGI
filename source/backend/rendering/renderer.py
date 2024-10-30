'''
Renderizador.
'''


from source.backend.math.screen import Conversor
from source.backend.math.vector import Vector
from source.backend.objects.object import Object
from source.backend.objects.window import Window
from source.backend.rendering.clipper import Clipper, LineClippingMethod
from source.backend.rendering.frame_generator import FrameGenerator


class Renderer():

    '''
    Renderizador.
    '''

    _bg_color: tuple[int, int, int]
    _clipper: Clipper
    _vireport_padding: Vector

    def __init__(self,
                 bg_color: tuple[int, int, int] = (0.05, 0.05, 0.05),
                 line_clipping_method: LineClippingMethod = LineClippingMethod.LIANG_BARSKY,
                 viewport_padding: Vector = Vector(25.0, 25.0, 0.0)) -> None:
        self._bg_color = bg_color
        self._clipper = Clipper(line_clipping_method)
        self._viewport_padding = viewport_padding

    @property
    def clipper(self) -> Clipper:
        '''
        Retorna o clipper.
        '''

        return self._clipper

    def render(self,
               area,
               context,
               screen_width: int,
               screen_height: int,
               window: Window,
               objects: Object) -> None:
        '''
        Método para a renderização.
        '''

        # Preenche o fundo
        context.set_source_rgb(self._bg_color[0], self._bg_color[1], self._bg_color[2])
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        FrameGenerator.generate_frame(window, objects)

        # Renderiza todos os objetos
        for object_ in objects + [window]:
            clipped_lines = []

            if object_ != window:
                clipped_lines = self._clipper.clip(window, object_)
            else:
                clipped_lines = object_.vector_lines

            screen_lines = list(map(lambda x: Conversor.world_line_to_screen(x,
                                                                             screen_width,
                                                                             screen_height,
                                                                             window,
                                                                             self._viewport_padding),
                                    clipped_lines))
            color = object_.color
            line_width = object_.line_width

            # Define cor e largura do pincel
            context.new_path()
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)

            if object_.fill and len(screen_lines) > 0:
                context.move_to(screen_lines[0][0].x, screen_lines[0][0].y)

            for line in screen_lines:
                if object_.fill:
                    context.line_to(line[1].x, line[1].y)
                else:
                    context.move_to(line[0].x, line[0].y)
                    context.line_to(line[1].x, line[1].y)
                    context.stroke()

            context.close_path()

            if object_.fill:
                context.fill()
