'''
Window.
'''

from source.backend.math.vector import Vector
from source.backend.objects.wireframes_2d import Rectangle


class Window(Rectangle):

    '''
    Janela.
    '''

    cop: Vector
    projected_cop: Vector
    projected_position: Vector

    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 cop: Vector,
                 color: tuple = (0.5, 0.0, 0.5),
                 line_width: float = 2.0) -> None:
        super().__init__(origin, extension, 'Window', color, line_width, False)

        self.cop = cop
        self.projected_cop = self.cop
        self.projected_position = self.position

    @property
    def origin(self) -> Vector:
        '''
        Retorna a coordenada da origem.
        '''

        return self.coords[0]

    @property
    def extension(self) -> Vector:
        '''
        Retorna a coordenada da extensão.
        '''

        return self.coords[2]

    @property
    def normalized_origin(self) -> Vector:
        '''
        Retorna a coordenada normalizada da origem.
        '''

        return self.normalized_coords[0]

    @property
    def normalized_extension(self) -> Vector:
        '''
        Retorna a coordenada normalizada da extensão.
        '''

        return self.normalized_coords[2]

    def calculate_x_axis(self) -> Vector:
        '''
        Calcula o eixo x da window.
        '''

        return self.coords[2] - self.coords[1]

    def calculate_y_vector(self) -> Vector:
        '''
        Retorna o vetor que aponta para cima.
        '''

        return self.coords[1] - self.coords[0]

    def calculate_z_vector(self) -> Vector:
        '''
        Retorna o vetor normal da window.
        '''

        return (self.calculate_x_axis() / 2.0).cross_product(self.calculate_y_vector() / 2.0)

    def calculate_x_projected_axis(self) -> Vector:
        '''
        Calcula o eixo x projetado da window.
        '''

        return self.projected_coords[2] - self.projected_coords[1]

    def calculate_y_projected_vector(self) -> Vector:
        '''
        Retorna o vetor projetado que aponta para cima.
        '''

        return self.projected_coords[1] - self.projected_coords[0]

    def calculate_z_projected_vector(self) -> Vector:
        '''
        Retorna o vetor normal projetado da window.
        '''

        return (self.calculate_x_projected_axis() / 2.0).cross_product(self.calculate_y_projected_vector() / 2.0)

    def calculate_cop_distance(self) -> float:
        '''
        Retorna a distância do cop (projetado) até o centro da window.
        '''

        return (self.projected_position - self.projected_cop).magnitude

    def translate(self, direction: Vector) -> None:
        coords = self._transform.translate(direction, self.coords + [self.cop])
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def rescale(self, scale: Vector) -> None:
        coords = self._transform.rescale(scale, self.coords + [self.cop])
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def rotate(self, rotation: Vector, origin: Vector | None = None) -> None:
        coords = self._transform.rotate(rotation, self.coords + [self.cop], origin)
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def project(self, cop: Vector, normal: Vector, cop_distance) -> None:
        coords = self._transform.project(cop, normal, cop_distance, self.coords + [cop, self.position], True)
        self.projected_coords = coords[:-2]
        self.projected_cop = coords[-2]
        self.projected_position = coords[-1]
