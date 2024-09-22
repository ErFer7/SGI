'''
Sistema Gráfico Interativo (SGI)
'''

import gi
gi.require_version('Gtk', '3.0')

#pylint: disable=wrong-import-position
from source.sgi import SGI

sgi = SGI()
sgi.run()
