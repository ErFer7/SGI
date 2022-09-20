# -*- coding: utf-8 -*-

'''
Módulo para o editor.
'''

import gi

from source.viewport import ViewportHandler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# As funcionalidades o button.py podem vir pra cá lentamente

class EditorHandler():

    '''
    Handler dos botões de edição.
    '''
