# -*- coding: utf-8 -*-

'''
Módulo para as operações matemáticas.
'''

import numpy as np

#TODO: Implementar
class Transform2D():

    '''
    Transformada.
    '''

    # Atributos ---------------------------------------------------------------
    #TODO: Usar uma matriz aqui.
    
    coord_list: list # lista de pontos (tuplas) que compõem o objeto
    rotation: float
    scale: list

    # Construtor --------------------------------------------------------------
    def __init__(self, coord_list: list = [(0.0, 0.0)], rotation: float = 0.0, scale: tuple = (1.0, 1.0)) -> None:

        self.coord_list = coord_list
        self.rotation = rotation
        self.scale = list(scale)

    # Getters e Seters --------------------------------------------------------
    @property
    def coord_list(self) -> list:
        '''
        Getter da posição.
        '''

        return self._coord_list

    @coord_list.setter
    def coord_list(self, value: list) -> None:
        '''
        Setter da posição.
        '''

        self._coord_list = value

    def translate(self, translation: tuple) -> list:
        '''
        Translação de um objeto. Retorna uma nova lista de coordenadas.
        '''
        new_coord_list: list = []
        for point in self.coord_list: # point = (x, y) ... new_point = (point[x] + t[x], point[y] + t[y])
            point = (point[0] + translation[0], point[1] + translation[1])
            new_coord_list.append(point)
        self.coord_list = new_coord_list
        return self.coord_list
