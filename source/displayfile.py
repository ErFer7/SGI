# -*- coding: utf-8 -*-

'''
Módulo para o handler do display file.
'''

from source.wireframe import Object, Point, Line, Wireframe


class DisplayFileHandler():

    '''
    Nesta classe os objetos seriam armazenados e transferidos para o viewport quando necessário.
    '''

    objects: list

    def __init__(self) -> None:

        self.objects = []
        self.add_object(Line((500, 500), (200, 300), "Test", (1, 0, 0), 2.0))  # Teste

    @property
    def objects(self) -> list:
        '''
        Getter dos objetos.
        '''

        return self._objects

    @objects.setter
    def objects(self, value: list) -> None:
        '''
        Setter dos objetos.
        '''

        self._objects = value

    def add_object(self, obj: list) -> None:  # object é keyword reservada
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
