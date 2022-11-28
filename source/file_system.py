# -*- coding: utf-8 -*-

'''
Módulo para o gerenciamento de arquivos.
'''

from source.wireframe import Object, Point, Line, Wireframe2D
from source.transform import Vector


class FileSystem():
    '''
    Sistema de arquivos.
    '''

    def load_scene(self, file_name: str) -> list[Object]:
        '''
        Carrega um arquivo.
        '''

        data_objects = []
        objects = []
        vertices = []
        materials = {}
        current_material = ''

        with open(file_name, 'r', encoding="utf-8") as file:

            for line in file.readlines():

                data = line.split()

                if len(data) > 0:

                    if data[0].startswith('#'):
                        continue

                    match data[0]:
                        case 'v':
                            vertices.append(Vector(float(data[1]), float(data[2]), float(data[3])))
                        case 'o':
                            data_objects.append(ObjectData(data[1]))
                        case 'p':
                            data_objects[-1].add_vertices([vertices[int(data[1]) - 1]])
                        case 'f':
                            pass
                        case 'w':
                            pass
                        case "mtllib":
                            pass
                        case "newmtl":
                            current_material = data[1]
                            materials[data[1]] = None
                        case "usemtl":
                            try:
                                data_objects[-1].add_material(materials[data[1]])
                            except KeyError:
                                print("[ERROR]: Material not found.")
                        case "Kd":
                            materials[current_material] = (float(data[1]), float(data[2]), float(data[3]))
                        case _:

                            valid = True
                            points = []

                            try:
                                points = list(map(int, data))
                            except ValueError:
                                valid = False

                            if valid:
                                obj_vertices = []

                                for point in points:
                                    obj_vertices.append(vertices[point - 1])

                                data_objects[-1].add_vertices(obj_vertices)
                            else:
                                print(f"Undefined OBJ argument: {data[0]}")

        for data_obj in data_objects:
            objects.append(data_obj.build_object())

        return objects

    def write_scene(self, file_name: str, objects: list[Object]) -> None:
        '''
        Escreve um arquivo.
        '''


class ObjectData():

    '''
    Descritor de objetos.
    '''

    _name: str
    _vertices: list[Vector]
    _material: tuple[float]

    def __init__(self, name: str) -> None:
        self._name = name
        self._vertices = []
        self._material = (1.0, 1.0, 1.0)

    def add_vertices(self, vertices: list[Vector]) -> None:
        '''
        Adiciona vértices.
        '''

        self._vertices = vertices

    def add_material(self, material: tuple[float]) -> None:
        '''
        Adiciona um material.
        '''

        self._material = material

    def build_object(self) -> Object:
        '''
        Processa os dados e gera um objeto.
        '''

        len_vertices = len(self._vertices)

        if len_vertices == 1:
            return Point(self._vertices[0], self._name, self._material)
        elif len_vertices == 2:
            return Line(self._vertices[0], self._vertices[1], self._name, self._material)
        else:
            return Wireframe2D(self._vertices, self._name, self._material)
