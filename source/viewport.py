# -*- coding: utf-8 -*-

'''
Neste módolo estão definidos os funcionamentos do viewport.
'''

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
import cairo


class Viewport():

    '''
    Definição do viewport, este viewport é um handler para um widget DrawingArea.
    '''

    # Handlers ----------------------------------------------------------------
    def on_draw(self, area, context) -> None:
        '''
        Método para a renderização
        '''

        # Código de testes

        context.scale(area.get_allocated_width(), area.get_allocated_height())  

        x0, y0 = 0.3, 0.3
        x1, y1 = 0.5, 0.5
        r0 = 0
        r1 = 1
        pattern = cairo.RadialGradient(x0, y0, r0, x1, y1, r1)
        pattern.add_color_stop_rgba(0, 1, 1, 0.5, 1)
        pattern.add_color_stop_rgba(1, 0.2, 0.4, 0.1, 1)
        context.rectangle(0, 0, 1, 1)
        context.set_source(pattern)
        context.fill()
        context.paint()
