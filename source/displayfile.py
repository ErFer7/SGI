# -*- coding: utf-8 -*-

'''
Módulo para o handler do display file.
'''

from source.wireframe import Object, Point, Line, Wireframe


class DisplayFileHandler():

    '''
    Nesta classe os objetos seriam armazenados e transferidos para o viewport quando necessário.
    '''

    # Atributos públicos
    objects: list

    def __init__(self) -> None:

        self.objects = []

    # Métodos utilitários
    def add_object(self, obj: Object) -> None:
        '''
        Adiciona um objeto.
        '''

        self.objects.append(obj)

    # Por enquanto o id é o nome
    def remove_object(self, identification: str) -> None:
        '''
        Remove um objeto.
        '''

        for obj in self.objects:

            if obj.identification == identification:
                self.objects.remove(obj)
                break
