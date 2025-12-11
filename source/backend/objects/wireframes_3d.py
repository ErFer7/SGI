"""
Módulo para wireframes 3D.
"""

import numpy as np

from source.backend.math.vector import Vector
from source.backend.objects.wireframes_2d import Object, ObjectType

import random
from noise import snoise2


class Wireframe3D(Object):
    """
    Wireframe 3D.
    """

    def __init__(
        self,
        coords: tuple[Vector],
        lines: tuple[tuple[int, int]],
        name: str = "",
        color: tuple = (1.0, 1.0, 1.0),
        line_width: float = 1.0,
        object_type: ObjectType = ObjectType.POLYGON3D,
    ) -> None:
        super().__init__(
            coords, lines, name, color, line_width, object_type, False, True
        )


class Parallelepiped(Wireframe3D):
    """
    Paralelepípedo.
    """

    def __init__(
        self,
        origin: Vector,
        extension: Vector,
        name: str = "",
        color: tuple = (1.0, 1.0, 1.0),
        line_width: float = 1.0,
    ) -> None:
        coords = (
            origin,
            Vector(origin.x, extension.y),
            extension,
            Vector(extension.x, origin.y),
            origin + Vector(0.0, 0.0, extension.x - origin.x),
            Vector(origin.x, extension.y, extension.x - origin.x),
            extension + Vector(0.0, 0.0, extension.x - origin.x),
            Vector(extension.x, origin.y, extension.x - origin.x),
        )

        lines = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
        )

        super().__init__(
            coords, lines, name, color, line_width, ObjectType.PARALLELEPIPED
        )


class Surface(Wireframe3D):
    """
    Superfície.
    """

    def __init__(
        self,
        points: tuple[Vector],
        steps: int,
        name: str = "",
        color: tuple = (1, 1, 1),
        line_width: float = 1,
        random: bool = False,
        rows: int = 10,
        cols: int = 10,
        spacing: float = 50,
        height_scale: float = 0.0,
        noise_scase: float = 0.0,
    ) -> None:
        if random:
            coords, lines = self.generate_perlin_surface_y(
                rows, cols, spacing, height_scale, noise_scase, steps
            )
        else:
            coords, lines = self.generate_surface_coords(points, steps)

        super().__init__(coords, lines, name, color, line_width, ObjectType.SURFACE)

    def generate_surface_coords(
        self, points: tuple[Vector], steps: int
    ) -> tuple[tuple[Vector], tuple[tuple[int, int]]]:
        """
        Gera uma superfície.
        """

        b_spline_matrix = (1 / 6) * np.matrix(
            [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]
        )

        b_spline_matrix_t = b_spline_matrix.getT()

        surface_coords = []
        lines = []

        for i, _ in enumerate(points):
            geometry_matrix_x = None
            geometry_matrix_y = None
            geometry_matrix_z = None

            if i + 15 < len(points):
                geometry_matrix_x = np.matrix(
                    [
                        [points[i + j].x for j in range(4)]
                        for i in range(0, len(points), 4)
                    ]
                )
                geometry_matrix_y = np.matrix(
                    [
                        [points[i + j].y for j in range(4)]
                        for i in range(0, len(points), 4)
                    ]
                )
                geometry_matrix_z = np.matrix(
                    [
                        [points[i + j].z for j in range(4)]
                        for i in range(0, len(points), 4)
                    ]
                )
            else:
                break

            line_index = 0
            fill_curve_a = True
            curve_a = []
            curve_b = []

            for step_s in range(steps):
                s = step_s / steps
                step_matrix_s = np.matrix([s**3, s**2, s, 1])
                for step_t in range(steps):
                    t = step_t / steps
                    step_matrix_t = np.matrix([[t**3], [t**2], [t], [1]])
                    new_x = (
                        step_matrix_s
                        * b_spline_matrix
                        * geometry_matrix_x
                        * b_spline_matrix_t
                        * step_matrix_t
                    )
                    new_y = (
                        step_matrix_s
                        * b_spline_matrix
                        * geometry_matrix_y
                        * b_spline_matrix_t
                        * step_matrix_t
                    )
                    new_z = (
                        step_matrix_s
                        * b_spline_matrix
                        * geometry_matrix_z
                        * b_spline_matrix_t
                        * step_matrix_t
                    )
                    surface_coords.append(Vector(new_x[0, 0], new_y[0, 0], new_z[0, 0]))

                    if line_index + 1 < len(surface_coords):
                        lines.append((line_index, line_index + 1))

                        if fill_curve_a:
                            curve_a.append(line_index)
                        else:
                            curve_b.append(line_index)
                        line_index += 1

                if fill_curve_a:
                    curve_a.append(line_index)
                else:
                    curve_b.append(line_index)

                if len(curve_a) > 0 and len(curve_b) > 0:
                    for index_a, index_b in zip(curve_a, curve_b):
                        lines.append((index_a, index_b))

                    curve_a = curve_b.copy()
                    curve_b.clear()

                line_index += 1
                fill_curve_a = False

        return (tuple(surface_coords), tuple(lines))

    def generate_perlin_surface_y(self, 
                              rows: int, 
                              cols: int, 
                              spacing: float, 
                              height_scale: float, 
                              noise_scale: float, 
                              steps: int) -> tuple[tuple[Vector], tuple[tuple[int, int]]]:
        
        # 1. Force minimum dimensions
        rows = max(4, rows)
        cols = max(4, cols)
        
        x_offset = random.uniform(0, 1000)
        z_offset = random.uniform(0, 1000)

        # --- 1. Generate Control Grid ---
        control_grid = []
        for r in range(rows):
            row_points = []
            for c in range(cols):
                x = c * spacing
                z = r * spacing
                
                # COORDINATE SCALING
                nx = (c / noise_scale) + x_offset
                nz = (r / noise_scale) + z_offset
                
                # --- MOUNTAIN ALGORITHM (Ridged Multifractal) ---
                
                # 1. Get noise (returns -1.0 to 1.0)
                # We use more octaves (6) for "rocky" detail
                n = snoise2(nx, nz, octaves=6, persistence=0.5, lacunarity=2.0)
                
                # 2. Absolute value creates sharp creases (valleys)
                n = abs(n)
                
                # 3. Invert so creases become peaks
                n = 1.0 - n
                
                # 4. Square it to flatten valleys and sharpen peaks
                n = n ** 2
                
                # Apply height
                y = n * height_scale
                # ------------------------------------------------
                
                row_points.append(Vector(x, y, z))
            control_grid.append(row_points)

        # 3. Setup B-Spline Matrices
        b_spline_matrix = (1 / 6) * np.matrix([[-1, 3, -3, 1],
                                               [3, -6, 3, 0],
                                               [-3, 0, 3, 0],
                                               [1, 4, 1, 0]])
        b_spline_matrix_t = b_spline_matrix.getT()

        # --- THE FIX STARTS HERE ---
        
        # Calculate the total size of the final vertex grid
        # This determines the size of our temporary 2D buffer
        final_rows = (rows - 3) * steps + 1
        final_cols = (cols - 3) * steps + 1
        
        # Create a 2D buffer to hold points in their correct geometric positions
        vertex_grid = [[None for _ in range(final_cols)] for _ in range(final_rows)]

        # Pre-calculate steps
        s_vectors = [np.matrix([v**3, v**2, v, 1]) for v in [i/steps for i in range(steps + 1)]]
        t_vectors = [np.matrix([[v**3], [v**2], [v], [1]]) for v in [i/steps for i in range(steps + 1)]]

        # 4. Generate Surface Patches
        for r in range(rows - 3):
            for c in range(cols - 3):
                
                # Geometry Matrices
                g_x = np.matrix([[control_grid[r+i][c+j].x for j in range(4)] for i in range(4)])
                g_y = np.matrix([[control_grid[r+i][c+j].y for j in range(4)] for i in range(4)])
                g_z = np.matrix([[control_grid[r+i][c+j].z for j in range(4)] for i in range(4)])
                
                bx_bt = b_spline_matrix * g_x * b_spline_matrix_t
                by_bt = b_spline_matrix * g_y * b_spline_matrix_t
                bz_bt = b_spline_matrix * g_z * b_spline_matrix_t

                # We iterate through the local steps of this patch
                # We don't need to skip edges anymore; overwriting the buffer is safer and simpler
                for step_u in range(steps + 1):
                    for step_v in range(steps + 1):
                        
                        vec_s = s_vectors[step_u]
                        vec_t = t_vectors[step_v]

                        new_x = vec_s * bx_bt * vec_t
                        new_y = vec_s * by_bt * vec_t
                        new_z = vec_s * bz_bt * vec_t
                        
                        # Map local patch step to global grid index
                        global_row = (r * steps) + step_u
                        global_col = (c * steps) + step_v
                        
                        # Store in the correct slot (overwriting is fine for shared edges)
                        if global_row < final_rows and global_col < final_cols:
                            vertex_grid[global_row][global_col] = Vector(new_x[0, 0], new_y[0, 0], new_z[0, 0])

        # 5. Flatten the 2D buffer into a 1D list
        # This ensures the points are perfectly ordered Row 0, then Row 1, etc.
        surface_coords = []
        for r in range(final_rows):
            for c in range(final_cols):
                if vertex_grid[r][c] is not None:
                    surface_coords.append(vertex_grid[r][c])

        # 6. Generate Topology (Lines)
        # The standard grid logic now works because the list order matches the geometric order
        lines = []
        for i in range(final_rows):
            for j in range(final_cols):
                current_idx = i * final_cols + j
                
                if j > 0: # Connect Left
                    lines.append((current_idx, current_idx - 1))
                if i > 0: # Connect Up
                    lines.append((current_idx, current_idx - final_cols))

        return (tuple(surface_coords), tuple(lines))

