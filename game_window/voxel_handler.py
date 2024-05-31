from constants import *
from meshes.chunk_mesh_builder import get_chunk_index
from random import randint

import rays


class VoxelHandler:
    def __init__(self, world):
        self.app = world.app
        self.chunks = world.chunks

        # ray casting result
        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_world_pos = None
        self.voxel_normal = None

        self.new_voxel_id = 1

        self.marker_mode = 0

        # self.ray_cast = rays.ray_cast

    def add_voxel(self):
        if self.voxel_id:
            # check voxel id along normal
            result = rays.get_voxel_id(self.voxel_world_pos + self.voxel_normal)
            if (self.voxel_world_pos + self.voxel_normal).y < 0:
                return

            # is the new place empty?
            if not result[0]:
                _, voxel_index, _, chunk = result
                chunk.voxels[voxel_index] = 1
                chunk.mesh.rebuild()

                # was it an empty chunk
                if chunk.is_empty:
                    chunk.is_empty = False

    def rebuild_adj_chunk(self, adj_voxel_pos):
        index = get_chunk_index(adj_voxel_pos)
        if index != -1:
            self.chunks[index].mesh.rebuild()

    def rebuild_adjacent_chunks(self):
        lx, ly, lz = self.voxel_local_pos
        wx, wy, wz = self.voxel_world_pos

        if lx == 0:
            self.rebuild_adj_chunk((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adj_chunk((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adj_chunk((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx, wy, wz + 1))

    def remove_voxel(self):
        if self.voxel_id:
            self.chunk.voxels[self.voxel_index] = 0

            self.chunk.mesh.rebuild()
            self.rebuild_adjacent_chunks()

    def set_voxel(self):
        self.add_voxel()

    def update(self):
        rc = rays.ray_cast(self.app.player.position, self.app.player.position + self.app.player.forward * MAX_RAY_DIST)
        self.voxel_id, self.voxel_index, self.voxel_local_pos, self.chunk, self.voxel_normal, self.voxel_world_pos = rc

