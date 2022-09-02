# -*- coding: utf-8 -*-

'''
Módolo para a interface de usuário.
'''

import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

@Gtk.Template(filename=os.path.join(os.getcwd(), "interface", "interface_style.ui"))
class MainWindow(Gtk.Window):

    '''
    Janela princial.
    '''
    __gtype_name__ = "MainWindow"

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        '''
        Fecha a janela.
        '''

        Gtk.main_quit()
