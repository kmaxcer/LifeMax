import numpy as np
from meshes.base_mesh import BaseMesh

class EmptyMesh(BaseMesh):
    def __init__(self):
        super().__init__()
        self.vbo_format = "3f 3f"
        self.attrs = ("in_position", "in_color")

    def get_vertex_data(self) -> np.array:
        # Создаем пустой массив вершин
        vertices = np.array([], dtype="f4")
        return vertices