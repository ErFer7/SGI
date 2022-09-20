# -*- coding: utf-8 -*-

'''
Módulo para o handler do display file.
'''

class DisplayFileHandler():

    object: list # [type, position, width, color] fazer uma classe pra isso?
    display_file: list = [] # lista de objetos

    def __init__(self):
        self.object = ["line", [[500, 500], [200, 300]], 3.0, [255, 0, 0]]
        self.display_file.append(self.object)

    def get_display_file(self):
        return self.display_file

    def add_object(self, object: list):
        self.display_file.append(object)

    def remove_object(self, object: list):
        # TO DO: remoção de objeto (por enquanto "object" não possui elemento "id")
        pass
