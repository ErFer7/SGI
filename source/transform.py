# -*- coding: utf-8 -*-

'''
Módulo para as operações matemáticas.
'''

import numpy as np


class Transform2D():

    '''
    Transformada.
    '''

    # Atributos ---------------------------------------------------------------
    
    coord_list: list # lista de pontos (tuplas) que compõem o objeto
    rotation: float
    scale: list

    t_matrix: np.array # translation matrix

    # Construtor --------------------------------------------------------------
    def __init__(self, coord_list: list = [(0.0, 0.0)], rotation: float = 0.0, scale: tuple = (1.0, 1.0)) -> None:

        self.coord_list = coord_list
        self.rotation = rotation
        self.scale = list(scale)

    # Getters e Setters --------------------------------------------------------
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

    # Transformações -----------------------------------------------------------
    def translate(self, translation: tuple) -> list:
        '''
        Translação de um objeto. Retorna uma nova lista de coordenadas.
        '''

        new_coord_list: list = []
        tx = translation[0]
        ty = translation[1]
        self.t_matrix = np.asarray([[1, 0, tx],
                                    [0, 1, ty],
                                    [0, 0, 1]])

        # Translação ponto a ponto
        for point in self.coord_list:
            x = point[0]
            y = point[1]
            new_coord = np.matmul(self.t_matrix, [x, y, 1])
            new_coord_list.append((new_coord[0], new_coord[1]))
        self.coord_list = new_coord_list
        print(self.coord_list)
        return self.coord_list
