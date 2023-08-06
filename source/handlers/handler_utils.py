# -*- coding: utf-8 -*-

'''
Módulo de utilidades para os handlers.
'''

import gi

gi.require_version('Gtk', '3.0')

# pylint: disable=wrong-import-position
from gi.repository import Gtk # type: ignore


class HandlerUtils():

    '''
    Utilidades para os handlers.
    '''

    @staticmethod
    def search_child_by_name(widget: Gtk.Widget, name: str) -> Gtk.Widget | None:
        '''
        Busca um widget pelo nome.
        '''

        if widget.get_name() == name:
            return widget

        if issubclass(type(widget), Gtk.Container):
            for child in widget.get_children():
                sub_widget = HandlerUtils.search_child_by_name(child, name)

                if sub_widget is not None:
                    return sub_widget

        return None
