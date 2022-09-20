# -*- coding: utf-8 -*-

'''
Módulo para as operações matemáticas.
'''

#TODO: Implementar
class Transform2D():

    '''
    Transformada.
    '''

    # Atributos ---------------------------------------------------------------
    #TODO: Usar uma matriz aqui.
    position: list
    rotation: float
    scale: list

    # Construtor --------------------------------------------------------------
    def __init__(self, position: tuple = (0.0, 0.0), rotation: float = 0.0, scale: tuple = (1.0, 1.0)) -> None:

        self.position = list(position)
        self.rotation = rotation
        self.scale = list(scale)

    # Getters e Seters --------------------------------------------------------
    @property
    def position(self) -> list:
        '''
        Getter da posição.
        '''

        return self._position

    @position.setter
    def position(self, value: list) -> None:
        '''
        Setter da posição.
        '''

        self._position = value
