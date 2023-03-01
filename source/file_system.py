# -*- coding: utf-8 -*-

'''
Módulo para o gerenciamento de arquivos.
'''

from source.wireframe import Object, Wireframe3D
from source.transform import Vector


class FileSystem():
    '''
    Sistema de arquivos.
    '''

    def load_scene(self, file_name: str) -> list[Object]:
        '''
        Carrega um arquivo.
        '''

        obj_file = ""
        mtl_file = ""

        try:
            with open(file_name, 'r', encoding="utf-8") as file:
                obj_file = file.readlines()
        except FileNotFoundError:
            print("File not found")

        try:
            with open(file_name[:-4] + ".mtl", 'r', encoding="utf-8") as file:
                mtl_file = file.readlines()
        except FileNotFoundError:
            pass

        data_objects = []
        objects = []
        vertices = []

        for line in obj_file:

            data = line.split()

            if len(data) > 0:

                if data[0].startswith('#'):
                    continue

                match data[0]:
                    case 'v':
                        vertices.append(Vector(float(data[1]), float(data[2]), float(data[3])))
                    case "vt":
                        pass
                    case "vn":
                        pass
                    case "vp":
                        pass
                    case "cstype":
                        pass
                    case "deg":
                        pass
                    case "bmat":
                        pass
                    case "step":
                        pass
                    case 'p':
                        index = int(data[1])
                        if index > 0:
                            index -= 1
                        data_objects[-1].add_vertices([vertices[index]])
                    case 'l':
                        data_objects[-1].add_vertex(int(data[1]))
                        data_objects[-1].add_vertex(int(data[2]))
                        data_objects[-1].add_lines((0, 1))
                    case 'f':

                        lines = []

                        v_list = []
                        vt_list = []
                        vn_list = []

                        for vector_set in data[1:]:
                            vectors = list(map(int, vector_set.split('/')))

                            if len(vectors) == 3:
                                v_list.append(vectors[0])
                                vt_list.append(vectors[1])
                                vn_list.append(vectors[2])
                            elif len(vectors) == 2:
                                if vector_set.count('/') == 2:
                                    v_list.append(vectors[0])
                                    vn_list.append(vectors[1])
                                else:
                                    v_list.append(vectors[0])
                                    vt_list.append(vectors[1])
                            else:
                                v_list.append(vectors[0])

                        offset = len(data_objects[-1].vertices)

                        for i, v in enumerate(v_list):

                            index = v
                            if index > 0:
                                index -= 1

                            data_objects[-1].add_vertex(vertices[index])

                            if i < len(v_list) - 1:
                                lines.append((offset + i, offset + i + 1))

                        lines.append((offset + len(v_list) - 1, offset + 0))

                        data_objects[-1].add_lines(lines)
                    case "curv":
                        pass
                    case "curv2":
                        pass
                    case "surf":
                        pass
                    case "parm":
                        pass
                    case "trim":
                        pass
                    case "hole":
                        pass
                    case "scrv":
                        pass
                    case "sp":
                        pass
                    case "end":
                        pass
                    case "con":
                        pass
                    case 'g':
                        pass
                    case 's':
                        pass
                    case "mg":
                        pass
                    case 'o':
                        data_objects.append(ObjectData(data[1]))
                    case "bevel":
                        pass
                    case "c_interp":
                        pass
                    case "d_interp":
                        pass
                    case "lod":
                        pass
                    case "usemtl":
                        pass
                    case "mtllib":
                        pass
                    case "shadow_obj":
                        pass
                    case "trace_obj":
                        pass
                    case "ctech":
                        pass
                    case "stech":
                        pass
                    case 'w':
                        pass
                    case "newmtl":
                        pass
                    case "Kd":
                        pass
                    case _:
                        pass

        for data_obj in data_objects:
            objects.append(data_obj.build_object())

        return objects

    def save_scene(self, file_name: str, objects: list[Object]) -> None:
        '''
        Escreve um arquivo.
        '''

        raise NotImplementedError


class ObjectData():

    '''
    Descritor de objetos.
    '''

    vertices: list[Vector]

    _name: str
    _lines: list[tuple[int]]
    _material: tuple[float]

    def __init__(self, name: str) -> None:
        self.vertices = []
        self._name = name
        self._lines = []
        self._lines = []
        self._material = (1.0, 1.0, 1.0)

    def add_vertex(self, vertex: Vector) -> None:
        '''
        Adiciona vértices.
        '''

        self.vertices.append(vertex)

    def add_lines(self, faces: list[tuple[int]]) -> None:
        '''
        Adiciona faces.
        '''

        self._lines += faces

    def add_material(self, material: tuple[float]) -> None:
        '''
        Adiciona um material.
        '''

        self._material = material

    def build_object(self) -> Object:
        '''
        Processa os dados e gera um objeto.
        '''

        return Wireframe3D(self.vertices, self._lines, self._name)
