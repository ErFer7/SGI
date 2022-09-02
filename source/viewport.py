# -*- coding: utf-8 -*-

'''
Neste módolo estão definidos os funcionamentos do viewport.
'''

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Viewport():

    '''
    Definição do viewport, este viewport é um container para um widget GLArea.
    '''

    gl_area: Gtk.GLArea

    def __init__(self, gl_area: Gtk.GLArea) -> None:
        self.gl_area = gl_area

    def on_render(self):
        '''
        Renderiza.
        '''
