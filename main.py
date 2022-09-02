# -*- coding: utf-8 -*-

'''
Sistema Gráfico Interativo (SGI)

Autores:
Eric Fernandes Evaristo (ErFer7)
Luis Henrique Goulart Stemmer (lust2k)
'''

VERSION = "v0.1-dev"
# -*- coding: utf-8 -*-

'''
Sistema Gráfico Interativo (SGI)
Autores:
Eric Fernandes Evaristo (ErFer7)
Luis Henrique Goulart Stemmer (lust2k)
'''

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

VERSION = "v0.1-dev"

from source.user_interface import MainWindow

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

