# -*- coding: utf-8 -*-

'''
Sistema Gráfico Interativo (SGI)

Autores da v1.0:
Eric Fernandes Evaristo (ErFer7)
Luis Henrique Goulart Stemmer (lust2k)

Autor da versão atual (v2.0):
Eric Fernandes Evaristo (ErFer7)
'''

import gi
gi.require_version('Gtk', '3.0')

#pylint: disable=wrong-import-position
from source.sgi import SGI

sgi = SGI()
sgi.run()
